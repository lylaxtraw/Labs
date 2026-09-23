# Guía de Uso - Sistema OLED con Animaciones GIF

## Instalación Rápida

### 1. Verificar Hardware

Conecta el Pico y ejecuta el diagnóstico:

```python
from tests.diagnostic import run_diagnostics
run_diagnostics()
```

Esto verificará:
- ✓ Frames PBM presentes (96 archivos)
- ✓ OLED funciona (blanco/negro)
- ✓ LEDs responden
- ✓ Botones detectan pulsaciones
- ✓ Frames pueden ser cargados

### 2. Convertir GIFs a PBM

Primero, asegúrate de tener Pillow instalada:

```bash
pip install Pillow
```

Luego convierte tus GIFs:

```bash
# Conversión simple (redimensiona automáticamente a 128x64)
python3 tools/gif_to_pbm.py happy.gif src/utils/scenes/scene0

python3 tools/gif_to_pbm.py sad.gif src/utils/scenes/scene1

python3 tools/gif_to_pbm.py angry.gif src/utils/scenes/scene2
```

Las imágenes se convierten a:
- Formato: PBM P4 (binario monocromático)
- Resolución: 128x64 píxeles
- Conversión: Escala de grises → B&N con dithering Floyd-Steinberg

### 3. Subir Frames al Pico

Los frames se suben automáticamente:

```bash
bash tools/upload_frames.sh
```

O manualmente para una escena específica:

```bash
# Subir todos los PBM de scene0
for i in {1..12}; do
  ampy --port /dev/cu.usbmodem11101 put "src/utils/scenes/scene0/$i.pbm" "utils/scenes/scene0/$i.pbm"
done
```

### 4. Ejecutar la Aplicación

Conecta al Pico y ejecuta:

```python
from main import main
main()
```

O simplemente, reinicia el Pico (Ctrl+D en REPL) para que `main.py` se ejecute automáticamente.

## Controles

- **Botón LEFT (Pin 2)**: Escena anterior
- **Botón RIGHT (Pin 3)**: Escena siguiente  
- **Botón PLAY (Pin 4)**: Play/Pause animación
- **Botón RESET (Pin 5)**: Volver a escena 0

## Indicadores LED

- **ROJO**: Parpadea al reiniciar
- **VERDE**: ON cuando animación está reproduciendo
- **AMARILLO**: ON/OFF según escena par/impar
- **AZUL**: Siempre ON (sistema activo)

## Estructura de Directorios

```
├── boot.py              # Inicialización de hardware
├── config.py            # Configuración de pines
├── main.py              # Punto de entrada
├── app.py               # Lógica de aplicación
├── lib/
│   ├── ssd1306.py       # Driver OLED
│   └── sfhm_pantallas.py # Utilidades de pantalla
└── utils/
    ├── animation.py     # Sistema de animación
    └── scenes/
        ├── scene0/      # Frames de escena 0 (1.pbm-12.pbm)
        ├── scene1/      # Frames de escena 1
        └── ... (scene2-7)
```

## Solución de Problemas

### "Loop termina después de unos segundos"

El sistema ahora tiene manejo de errores mejorado. Si el loop se cierra:
1. Ejecuta el diagnóstico
2. Revisa los mensajes de error
3. Verifica que los frames existan

### "Botones no responden"

1. Ejecuta `run_diagnostics()` y mira la prueba de botones
2. Verifica que los pines sean correctamente asignados en `config.py`
3. Comprueba las conexiones físicas de los botones

### "Frames no se ven o se ven mal"

1. Verifica que el GIF original sea de tamaño apropiado (idealmente 128x64 o múltiplo)
2. Intenta regenerar con: `python3 tools/gif_to_pbm.py input.gif output_dir --resize`
3. Carga un frame de prueba manualmente en el REPL:

```python
from utils.animation import PBMAnimation
from boot import init_display
oled = init_display()
anim = PBMAnimation(oled, 0)
anim.play_frame(0)
```

## Ejemplo Completo

```bash
# 1. Convertir GIFs
python3 tools/gif_to_pbm.py animations/happy.gif src/utils/scenes/scene0 --resize
python3 tools/gif_to_pbm.py animations/sad.gif src/utils/scenes/scene1 --resize

# 2. Subir a Pico
bash tools/upload_frames.sh

# 3. Conectar y ejecutar
# (usa minicom o similar)
# from main import main
# main()
```

## Parámetros Configurables

En `config.py`:

- `FRAME_DELAY_MS`: Delay entre frames (default: 100ms)
- `NUM_SCENES`: Número de emociones (default: 8)
- `NUM_FRAMES`: Frames por escena (default: 12)
- `BTN_LEFT`, `BTN_RIGHT`, `BTN_PLAY`, `BTN_RESET`: Asignación de pines
- `LED_RED`, `LED_GREEN`, `LED_YELLOW`, `LED_BLUE`: LEDs

