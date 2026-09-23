# Lab 4: Sistema de Animación OLED con GIFs

Sistema completo para mostrar **animaciones GIF en una pantalla OLED** con control mediante **4 botones** y **feedback con LEDs**.

Convierte automáticamente GIFs → fotogramas PBM → pantalla OLED

## 🎯 Características

- ✅ Conversión automática de GIFs a fotogramas (128×64, monocromático)
- ✅ **4 GIFs incluidos en `img/`** (listos para convertir)
- ✅ Hasta 8 escenas con 12 fotogramas cada una
- ✅ Control por 4 botones (siguiente, anterior, play/pause, reset)
- ✅ Feedback visual con 4 LEDs
- ✅ Loop principal robusto
- ✅ Herramienta de diagnóstico integrada

---

## 📋 Requisitos Previos

### Hardware
- Raspberry Pi Pico (RP2040)
- Pantalla OLED SSD1306 (128×64, I2C)
- 4 Botones (pull-up)
- 4 LEDs con resistencias 220Ω
- Conexión USB

### Software
- Python 3.7+
- Pillow: `pip install Pillow`
- adafruit-ampy: `pip install adafruit-ampy`

---

## 🚀 Guía Rápida

### Paso 1: Verificar Hardware ✓

Conecta el Pico por USB y ejecuta:

```bash
# Subir test rápido
ampy --port /dev/cu.usbmodem11101 put tests/simple_test.py tests/simple_test.py

# Conectar a REPL (minicom, screen, etc.)
from tests.simple_test import quick_test
quick_test()
```

**Resultado esperado:**
- OLED cambia a **blanco** (pantalla clara)
- OLED cambia a **negro** (pantalla oscura)  
- OLED muestra **patrón de cruz**

✅ **Si ves los cambios:** OLED funciona correctamente  
❌ **Si no ves nada:** Revisa conexiones I2C (pins 14/15)

---

### Paso 2: Convertir GIFs a Animaciones

Los GIFs están en `img/`:

```bash
ls -lh img/
# 07f64dd82f0bcc2fe71d68187c2c98bf.gif  (15 frames)
# 0d7623526d39e7710d8c965a1715f8b4.gif  (101 frames)
# 12af055ae2e3384b204d192b4f835cca.gif  (157 frames)
# 2ca59c6630e4e881a91d8b00c0913bc7.gif  (153 frames)
```

**Convertir todos:**

```bash
# Automático (usa solo 12 frames de cada GIF)
python3 tools/gif_to_pbm.py img/07f64dd82f0bcc2fe71d68187c2c98bf.gif src/utils/scenes/scene0
python3 tools/gif_to_pbm.py img/0d7623526d39e7710d8c965a1715f8b4.gif src/utils/scenes/scene1
python3 tools/gif_to_pbm.py img/12af055ae2e3384b204d192b4f835cca.gif src/utils/scenes/scene2
python3 tools/gif_to_pbm.py img/2ca59c6630e4e881a91d8b00c0913bc7.gif src/utils/scenes/scene3
```

**O en bash:**

```bash
for i in 0 1 2 3; do
  gif=$(ls img/*.gif | sed -n "$((i+1))p")
  python3 tools/gif_to_pbm.py "$gif" "src/utils/scenes/scene$i"
done
```

---

### Paso 3: Subir Frames y Código al Pico

```bash
# Subir código Python
bash tools/upload.sh /dev/cu.usbmodem11101

# Subir fotogramas (animaciones)
bash tools/upload_frames.sh /dev/cu.usbmodem11101
```

---

### Paso 4: Ejecutar la Aplicación

**Opción A - Manual (desde REPL):**

```python
from main import main
main()
```

**Opción B - Automático:**
- Presiona Ctrl+D en el REPL (reinicia el Pico)
- `main.py` se ejecuta automáticamente

---

## 🎮 Controles

| Botón | Pin | Acción |
|-------|-----|--------|
| **LEFT** | 2 | Escena anterior |
| **RIGHT** | 3 | Escena siguiente |
| **PLAY** | 4 | Play/Pause animación |
| **RESET** | 5 | Volver a escena 0 |

---

## 💡 Indicadores LED

| LED | Pin | Estado |
|-----|-----|--------|
| **ROJO** | 6 | Parpadea al reiniciar |
| **VERDE** | 7 | ON = animación reproduciendo |
| **AMARILLO** | 8 | ON = escena par, OFF = escena impar |
| **AZUL** | 9 | ON = sistema activo |

---

## 📦 Herramientas

### `manager.sh` - Gestor Completo

```bash
# Ver opciones
bash manager.sh help

# Diagnóstico del sistema
bash manager.sh test

# Convertir GIF a escena
bash manager.sh convert img/mi_gif.gif 0

# Subir todos los frames
bash manager.sh upload-frames

# Ejecutar aplicación
bash manager.sh run

# Todo en uno
bash manager.sh quick img/mi_gif.gif 0
```

### `tools/gif_to_pbm.py` - Conversor de GIFs

```bash
python3 tools/gif_to_pbm.py input.gif output_dir [--resize]

# Ejemplos:
python3 tools/gif_to_pbm.py happy.gif src/utils/scenes/scene0
python3 tools/gif_to_pbm.py sad.gif src/utils/scenes/scene1 --resize
```

### `tests/simple_test.py` - Tests Rápidos

```python
from tests.simple_test import quick_test, test_buttons, test_all

# Test rápido de OLED
quick_test()

# Test de botones (10 segundos)
test_buttons()

# Todas las pruebas
test_all()
```

---

## 📁 Estructura de Archivos

```
lab4/
├── img/                          # GIFs originales
│   ├── 07f64dd82f0bcc2fe71d68187c2c98bf.gif   (15 frames)
│   ├── 0d7623526d39e7710d8c965a1715f8b4.gif   (101 frames)
│   ├── 12af055ae2e3384b204d192b4f835cca.gif   (157 frames)
│   └── 2ca59c6630e4e881a91d8b00c0913bc7.gif   (153 frames)
│
├── src/                          # Código fuente
│   ├── boot.py                   # Inicialización de hardware
│   ├── config.py                 # Configuración de pines
│   ├── main.py                   # Punto de entrada
│   ├── app.py                    # Lógica de aplicación
│   ├── lib/
│   │   ├── ssd1306.py            # Driver OLED
│   │   └── sfhm_pantallas.py    # Utilidades de pantalla
│   └── utils/
│       ├── animation.py          # Sistema de animación
│       └── scenes/               # Fotogramas (48 total)
│           ├── scene0/           # GIF 1 (12 fotogramas)
│           ├── scene1/           # GIF 2 (12 fotogramas)
│           ├── scene2/           # GIF 3 (12 fotogramas)
│           ├── scene3/           # GIF 4 (12 fotogramas)
│           ├── scene4-7/         # Vacíos (opcional)
│
├── tests/                        # Tests y diagnósticos
│   ├── simple_test.py            # Test rápido de OLED
│   └── diagnostic.py             # Diagnóstico completo
│
├── tools/                        # Scripts de utilidad
│   ├── gif_to_pbm.py             # Conversor GIF→PBM
│   ├── upload.sh                 # Subir código
│   ├── upload_frames.sh          # Subir fotogramas
│   └── generate_test_frames.py   # Generar frames de prueba
│
├── manager.sh                    # Gestor completo
├── START.sh                      # Guía de inicio rápido
├── SETUP_GUIDE.md               # Guía detallada
└── README.md                     # Este archivo
```

---

## 🔧 Solución de Problemas

### OLED no muestra nada

1. **Verificar conexiones I2C:**
   ```
   SDA → Pin 14
   SCL → Pin 15
   GND → GND
   VCC → 3V3
   ```

2. **Probar con test simple:**
   ```python
   from tests.simple_test import quick_test
   quick_test()
   ```

3. **Revisar dirección I2C:**
   ```python
   from machine import I2C, Pin
   i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
   print(i2c.scan())  # Debe mostrar [60] (0x3C)
   ```

---

### Botones no responden

1. **Verificar pines en config.py:**
   - LEFT: Pin 2 ✓
   - RIGHT: Pin 3 ✓
   - PLAY: Pin 4 ✓
   - RESET: Pin 5 ✓

2. **Test de botones:**
   ```python
   from tests.simple_test import test_buttons
   test_buttons()
   ```

---

### Frames no se cargan o se ven mal

1. **Verificar que existen:**
   ```bash
   ls src/utils/scenes/scene0/
   # Debe mostrar: 1.pbm, 2.pbm, ..., 12.pbm
   ```

2. **Verificar en Pico:**
   ```python
   import os
   print(os.listdir('utils/scenes/scene0'))
   ```

3. **Probar cargar un frame manualmente:**
   ```python
   from utils.animation import PBMAnimation
   from boot import init_display
   oled = init_display()
   anim = PBMAnimation(oled, 0)
   anim.play_frame(0)
   ```

---

### Loop se cierra prematuramente

El loop ahora es robusto y continúa aunque haya errores. Si se cierra:

1. **Revisa mensajes de error en REPL**
2. **Ejecuta diagnóstico completo:**
   ```python
   from tests.diagnostic import run_diagnostics
   run_diagnostics()
   ```
3. **Verifica que todos los imports funcionan:**
   ```python
   from main import main
   from boot import init_display, init_buttons, init_leds
   from utils.animation import PBMAnimation
   ```

---

## 📊 Parámetros Configurables

En `src/config.py`:

- `FRAME_DELAY_MS`: Delay entre fotogramas (default: 100ms)
- `NUM_SCENES`: Número de escenas (default: 8)
- `NUM_FRAMES`: Fotogramas por escena (default: 12)
- `I2C_SDA`, `I2C_SCL`: Pines I2C
- `BTN_*`: Pines de botones
- `LED_*`: Pines de LEDs

---

## 🎨 Formato de Imágenes

- **Formato**: PBM P4 (binario monocromático)
- **Resolución**: 128×64 píxeles
- **Conversión automática**: GIF → escala de grises → B&N (dithering Floyd-Steinberg)
- **Tamaño por frame**: 1034 bytes
- **Total 4 escenas**: ~48 KB

---

## 📚 Referencias

- [Raspberry Pi Pico Docs](https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html)
- [MicroPython Docs](https://docs.micropython.org/)
- [SSD1306 Datasheet](https://cdn-shop.adafruit.com/datasheets/SSD1306.pdf)
- [Pillow (PIL) Docs](https://pillow.readthedocs.io/)

---

## 📝 Notas Finales

- ✅ OLED funciona (verificado con quick_test)
- ✅ 4 GIFs convertidos a 12 frames cada uno
- ✅ 48 fotogramas listos en Pico
- ✅ Sistema robusto contra errores
- 🎮 Ahora prueba los botones para navegar entre animaciones

**Siguiente paso:** Presiona los botones y disfruta las animaciones! 🎨

**Última actualización**: 2026-09-23  
**Estado**: ✅ Completamente funcional
