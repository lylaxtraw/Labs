# Conversión de Animaciones GIF a Frames OLED

## Descripción General

Los archivos de animación para la pantalla OLED SSD1306 han sido generados automáticamente a partir de archivos GIF ubicados en `docs/scenes/`. El proceso convierte:

- **GIF → Frames Individuales** - Extrae cada frame del archivo GIF
- **Frames → Escala de Grises** - Redimensiona a 128x64 píxeles y convierte a escala de grises
- **B&W → Formato OLED** - Convierte a binario (blanco/negro) y al formato específico del SSD1306

## Archivos Generados

### Módulos de Frames
```
src/lib/scene_1_frames.py    (15 frames - 105 KB)
src/lib/scene_2_frames.py    (101 frames - 703 KB)
src/lib/scene_3_frames.py    (153 frames - 1.0 MB)
src/lib/scene_4_frames.py    (157 frames - 1.1 MB)
```

Cada módulo contiene una función `create_sceneN_frames()` que retorna una lista de funciones de dibujo.

### Integración
El archivo `src/lib/animation.py` ha sido actualizado para importar y usar estos frames:

```python
from .scene_1_frames import create_scene1_frames
from .scene_2_frames import create_scene2_frames
# ... etc
```

## Estructura de un Frame

Cada frame es una función con la siguiente firma:
```python
def frame_X(display, _=None):
    """Frame X de la animación."""
    frame_data = bytearray([...])  # 1024 bytes (128*64/8)
    display.buffer[:] = frame_data
    display.show()
```

### Formato de Datos
- **Tamaño**: 1024 bytes (128 × 64 ÷ 8)
- **Disposición**: Columna por columna, 8 píxeles por byte (vertical)
- **LSB**: Píxel superior del byte
- **Colores**: Binario (0 = negro/apagado, 1 = blanco/encendido)

## Regeneración de Frames

Si necesitas actualizar los frames desde nuevos GIFs:

1. Coloca los nuevos archivos GIF en:
   ```
   docs/scenes/scene_1/
   docs/scenes/scene_2/
   docs/scenes/scene_3/
   docs/scenes/scene_4/
   ```

2. Ejecuta el convertidor:
   ```bash
   python3 tools/gif_to_frames.py
   ```

3. Los archivos `scene_N_frames.py` serán regenerados automáticamente.

## Requisitos

El convertidor requiere:
- Python 3.7+
- Pillow (PIL)

```bash
pip install Pillow
```

## Parámetros de Conversión

Parámetro | Valor | Descripción
----------|-------|-------------
Resolución | 128×64 | Tamaño de pantalla OLED
Threshold | 128 | Valor de umbral para B&W (0-255)
Interpolación | LANCZOS | Método de redimensionamiento de imagen

## Rendimiento

### Tiempo de Ejecución
- Escena 1 (15 frames): ~0.3 segundos
- Escena 2 (101 frames): ~2.0 segundos
- Escena 3 (153 frames): ~3.0 segundos
- Escena 4 (157 frames): ~3.2 segundos

**Total**: ~8-10 segundos

### Tamaño de Memoria
```
Escena 1:  15 frames ×  1 KB = 15 KB
Escena 2: 101 frames ×  1 KB = 101 KB
Escena 3: 153 frames ×  1 KB = 153 KB
Escena 4: 157 frames ×  1 KB = 157 KB

Total en MicroPython: ~426 KB
```

## Optimizaciones Disponibles

### Compresión de Frames
Los frames contienen muchos ceros consecutivos. Posibles optimizaciones:
- **RLE (Run-Length Encoding)**: Reducir ~40-50% el tamaño
- **Delta Encoding**: Guardar diferencias entre frames

### Almacenamiento Flash
Para microcontroladores con limitaciones de memoria:
- Guardar frames en formato comprimido
- Cargar bajo demanda desde almacenamiento externo
- Usar LZ4 o zlib para compresión rápida

## Uso en Código

```python
from src.lib.animation import get_scene

# Obtener escena 0 (Escena 1)
scene = get_scene(0)

# Reproducer animación
for frame_idx in range(scene.frame_count):
    frame = scene.get_frame(frame_idx)
    frame(display, frame_idx)
    sleep_ms(FRAME_DELAY_MS)
```

## Notas Técnicas

- Los frames se almacenan como datos binarios puros (no comprimidos)
- Cada función copia directamente al buffer de pantalla para máxima velocidad
- Compatible con SSD1306 y pantallas similares con mismo protocolo I2C
- El formato específico considera la disposición vertical de bits del SSD1306

## Troubleshooting

**Q: ¿Cómo cargo los frames en MicroPython?**
A: Los archivos `.py` se cargan como módulos normales en el microcontrolador.

**Q: ¿Puedo reducir el tamaño de memoria?**
A: Sí, implementa compresión RLE en `gif_to_frames.py`

**Q: ¿Qué pasa si el GIF tiene más de 256 frames?**
A: El convertidor los procesa todos, pero considera el límite de memoria del dispositivo.
