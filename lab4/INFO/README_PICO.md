# 🎬 Proyecto OLED Animado - Raspberry Pi Pico

## ✅ Estado Actual

El proyecto está **completamente optimizado y listo para la Pico**:

- ✅ 426 frames convertidos a datos comprimidos (RLE)
- ✅ Organizado en 4 escenas (15, 101, 153, 157 frames)
- ✅ Segmentado en módulos pequeños (8 frames/archivo)
- ✅ Carga lazy en todos los niveles (sin MemoryError)
- ✅ Tamaño total: **0.97 MB** (cabe en Pico)

## 🚀 Cómo Instalar en tu Pico

### Paso 1: Preparar la Pico

```bash
# Conecta la Pico por USB
# Entra en REPL (Ctrl+C en algunos casos)
# O abre terminal:
screen /dev/tty.usbmodem* 115200
```

### Paso 2: Transferir Archivos

Ya hemos creado la carpeta `pico_distribution/` con todos los archivos necesarios.

**Opción A - Con rshell (Recomendado):**

```bash
# Instalar rshell si no lo tienes
pip install rshell

# Transferir
rshell
> ls /pyboard/                    # Ver qué hay en Pico
> rm -r /pyboard/*                # Limpiar si es necesario
> cp -r pico_distribution/* /pyboard/
> exit
```

**Opción B - Manualmente con Thonny:**
1. Abre Thonny → Interpreter → MicroPython (Raspberry Pi Pico)
2. En Files, copia carpeta por carpeta desde `pico_distribution/`

### Paso 3: Verificar Instalación

En el REPL de la Pico:

```python
# Ver archivos en raíz
>>> import os
>>> os.listdir('/')
['boot.py', 'main.py', 'config.py', 'lib', 'docs']  # Debe verse así

# Verificar que hay datos de escenas
>>> os.listdir('/docs/scenes/scene_3/')
['scene_3_frames.py', 'scene_3_frames_part0.py', ...]
```

## 🧪 Pruebas Incrementales

### Test 1: Verificar OLED Funciona

```python
# En el REPL de Pico
>>> from machine import I2C, Pin
>>> i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400_000)
>>> devices = i2c.scan()
>>> print([hex(d) for d in devices])
['0x3c']  # Si ve 0x3C, el OLED está conectado
```

### Test 2: Probar Pantalla

```python
>>> from lib.ssd1306 import OLED_SSD1306
>>> oled = OLED_SSD1306(i2c, address=0x3C, width=128, height=64)
>>> oled.fill(0)
>>> oled.show()
# Debe limpiar la pantalla

# Dibujar línea
>>> for x in range(0, 128, 2):
...     oled.pixel(x, 32, 1)
>>> oled.show()
# Debe ver una línea horizontal
```

### Test 3: Probar Animación

```python
# Importar
>>> from lib.animation import get_scene
>>> scene = get_scene(2)  # Scene 3 (la más grande - 153 frames)
>>> print(scene.name)
Escena 3 - Animación desde GIF

# Obtener un frame
>>> frame = scene.get_frame(0)
>>> print(type(frame).__name__)
function

# Dibujar en pantalla
>>> frame(oled, 0)
>>> oled.show()
# Debe ver un frame dibujado en la OLED
```

### Test 4: Ejecutar Animación Completa

```python
# Ejecutar el programa principal
>>> exec(open('main.py').read())
# Verás mensajes de debug en el REPL
# Y la animación en la OLED
```

## 🔴 Solución de Problemas

### Problema: "No module named 'boot'"

- ✓ Verifica que `boot.py`, `config.py` y `main.py` están en la raíz (`/`)
- ✓ Prueba `os.listdir('/')` en el REPL

### Problema: "OLED No Muestra Nada"

1. Verifica que OLED está detectado: `i2c.scan()` debe mostrar `[60]` (0x3C en decimal)
2. Verifica pines:
   - SDA = GPIO 14 (pin 9)
   - SCL = GPIO 15 (pin 10)
   - GND = GND (pin 3 o 8)
   - VCC = 3.3V (pin 36)
3. Prueba el script `test_oled.py` si lo copiaste

### Problema: "MemoryError allocating..."

- El sistema lazy loading debe evitar esto
- Si lo ves, intenta:
  ```python
  # Ejecutar un reset suave
  >>> import machine
  >>> machine.soft_reset()
  ```

### Problema: Los Botones No Funcionan

Verifica en `config.py`:
```python
BUTTON_SCENE_1 = Pin(10, Pin.IN, Pin.PULL_UP)  # Scene 1
BUTTON_SCENE_2 = Pin(16, Pin.IN, Pin.PULL_UP)  # Scene 2
BUTTON_SCENE_3 = Pin(17, Pin.IN, Pin.PULL_UP)  # Scene 3
BUTTON_SCENE_4 = Pin(11, Pin.IN, Pin.PULL_UP)  # Scene 4
```

## 📊 Información de Tamaño

```
Scene 1 (15 frames):   ~30 KB
Scene 2 (101 frames):  ~300 KB
Scene 3 (153 frames):  ~450 KB
Scene 4 (157 frames):  ~220 KB (frames más pequeños)
─────────────────────────────
Total:                 ~1.0 MB

Almacenamiento Pico:   2 MB
Disponible después:    ~1 MB ✅
```

## 🎮 Controles

Una vez que ejecutes `main.py`:

| Botón | GPIO | Acción |
|-------|------|--------|
| Button 1 | GPIO 10 | Scene 1 |
| Button 2 | GPIO 16 | Scene 2 |
| Button 3 | GPIO 17 | Scene 3 |
| Button 4 | GPIO 11 | Scene 4 |

Presiona cualquier botón para cambiar de escena.

## 📝 Logs de Debug

Cuando ejecutes `main.py`, verás mensajes como:

```
MicroPython - Iniciando aplicación de animación OLED
==================================================
Importando boot...
Inicializando pantalla OLED...
✓ Pantalla OLED inicializada
✓ Pantalla limpiada
✓ Iniciando con escena 0
Bucle principal activo...
✓ Frames mostrados: 100, Escena: 0, Frame: 0
✓ Frames mostrados: 200, Escena: 0, Frame: 50
...
```

## 🎯 Próximos Pasos

1. **Copiar carpeta `pico_distribution/` a Pico** ← Estás aquí
2. Probar OLED en REPL (Test 1 y 2)
3. Probar animación en REPL (Test 3 y 4)
4. Crear `boot.py` en raíz si quieres que se ejecute automáticamente
5. Ajustar `FRAME_DELAY_MS` en config.py si quieres cambiar velocidad

## ❓ Preguntas Frecuentes

**P: ¿Por qué tarda en cargar la first scene?**
A: La primera carga descarga el primer segmento (8 frames) del almacenamiento. Es normal.

**P: ¿Puedo cambiar la velocidad de animación?**
A: Sí. En `config.py`, cambia `FRAME_DELAY_MS = 100` (está en milisegundos).

**P: ¿Funciona sin botones?**
A: Sí. Los botones son opcionales. Sin ellos, solo play la primera escena en loop.

**P: ¿Cómo puedo volver al REPL desde la animación?**
A: Presiona Ctrl+C en la terminal para detener `main.py`.

---

**¡Listo! Tu Pico está preparada. Copia la carpeta y pruébala.** 🚀
