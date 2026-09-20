# 📱 Guía de Instalación en Raspberry Pi Pico

## Estructura de Archivos Esperada en la Pico

La Pico debe tener esta estructura (en su filesystem montado como `/`):

```
/
├── main.py                 ← Punto de entrada (MicroPython lo ejecuta)
├── boot.py                 ← Módulo de animación
├── config.py               ← Configuración de pines
├── lib/
│   ├── animation.py
│   ├── ssd1306.py
│   └── my_lib.py
└── docs/
    └── scenes/
        ├── scene_1/
        │   ├── scene_1_frames.py
        │   ├── scene_1_frames_part0.py
        │   └── scene_1_frames_part1.py
        ├── scene_2/
        │   ├── scene_2_frames.py
        │   ├── scene_2_frames_part0.py
        │   └── ...
        ├── scene_3/
        │   ├── scene_3_frames.py
        │   ├── scene_3_frames_part0.py
        │   └── ...
        └── scene_4/
            ├── scene_4_frames.py
            ├── scene_4_frames_part0.py
            └── ...
```

## Pasos para Instalar

### 1. Preparar el Proyecto Localmente

Ejecuta este script para copiar archivos correctamente:

```bash
# Desde la carpeta del proyecto
cp src/main.py main.py              # Crear main.py en raíz
cp src/boot.py boot.py              # Crear boot.py en raíz
cp src/config.py config.py          # Crear config.py en raíz
cp -r src/lib lib                   # Copiar carpeta lib
cp -r docs docs                     # Copiar carpeta docs (con frames)
```

### 2. Conectar Pico en Modo REPL (Recommended for Debugging)

```bash
# Ver puerto serial
ls /dev/tty.usbmodem*

# Conectar con minicom/screen
screen /dev/tty.usbmodem14101 115200
```

### 3. Transferir Archivos a Pico

**Opción A: Usar `rshell` (Recomendado)**

```bash
pip install rshell
rshell
> cp main.py /pyboard/
> cp boot.py /pyboard/
> cp config.py /pyboard/
> cp -r lib /pyboard/
> cp -r docs /pyboard/
> repl
```

**Opción B: Usar Thonny IDE**
1. Abre Thonny
2. Selecciona "Tools" > "Options" > "Interpreter"
3. Elige "MicroPython (Raspberry Pi Pico)"
4. En la pestaña "Files", copia/pega los archivos

### 4. Ejecutar en Pico

En el REPL de MicroPython:

```python
# Ver si los archivos están
import os
os.listdir('/')

# Ejecutar el script de prueba primero
exec(open('/tools/test_oled.py').read())

# Si todo funciona, ejecutar la animación:
exec(open('main.py').read())
```

## 🔧 Solución de Problemas

### Problema: "No module named 'main'"

**Solución**: Asegúrate de que `main.py` está en la raíz (`/`), no en `/src/`.

### Problema: OLED no muestra nada

1. Ejecuta `test_oled.py` para diagnosticar
2. Verifica conexión I2C (SDA=GPIO14, SCL=GPIO15)
3. Comprueba que la dirección es 0x3C (o 0x3D)

### Problema: "MemoryError: memory allocation failed"

- Los archivos están copiados correctamente?
- ¿Hay suficiente espacio en Pico? (Usa `os.statvfs('/')``)
- Ejecuta prueba incremental: primero `test_oled.py`, luego `main.py`

### Problema: Los botones no funcionan

Verifica en `config.py`:
- BUTTON_SCENE_1 = Pin(10, Pin.IN, Pin.PULL_UP)
- BUTTON_SCENE_2 = Pin(16, Pin.IN, Pin.PULL_UP)
- BUTTON_SCENE_3 = Pin(17, Pin.IN, Pin.PULL_UP)
- BUTTON_SCENE_4 = Pin(11, Pin.IN, Pin.PULL_UP)

## 📊 Información de Tamaño

Los frames ocupan aproximadamente:

- Scene 1 (15 frames): ~50KB
- Scene 2 (101 frames): ~300KB
- Scene 3 (153 frames): ~450KB
- Scene 4 (157 frames): ~470KB
- **Total**: ~1.2MB (De ~2.9MB inicial, gracias a RLE compression)

La Pico tiene 2MB de almacenamiento, lo que da margen.

## ✅ Verificación Final

```python
# En el REPL de la Pico
import os
from lib.animation import get_scene

# Verificar estructura
print(os.listdir('/'))           # Ver archivos en raíz
print(os.listdir('/docs'))       # Ver carpeta docs

# Probar carga de escenas
scene = get_scene(2)             # Scene 3 (la más pesada)
print(scene.name)                # Debe imprimir "Escena 3..."
frame = scene.get_frame(0)       # Obtener primer frame
print(type(frame).__name__)      # Debe imprimir "function"
```

Si todo funciona, ejecuta `exec(open('main.py').read())` para iniciar la animación.
