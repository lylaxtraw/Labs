# Lab 4: Animación OLED con Selección de Escenas

Proyecto de MicroPython para una Raspberry Pi Pico basada en el microcontrolador
RP2040. El proyecto muestra animaciones en una pantalla OLED mediante secuencias
de imágenes. Utiliza cuatro interruptores para seleccionar entre cuatro escenas
animadas diferentes.

- Presionar el interruptor 1 selecciona la **Escena 1: Círculos Animados**
- Presionar el interruptor 2 selecciona la **Escena 2: Líneas Dinámicas**
- Presionar el interruptor 3 selecciona la **Escena 3: Rectángulos Rotantes**
- Presionar el interruptor 4 selecciona la **Escena 4: Patrón Parpadeante**

Cada escena reproduce una secuencia de 12 frames en loop continuo.

## Hardware

### Pantalla OLED SSD1306

| Conexión | GPIO | Descripción |
| --- | ---: | --- |
| SDA | 4 | Línea de datos I2C |
| SCL | 5 | Línea de reloj I2C |
| GND | GND | Tierra |
| VCC | 3.3V | Alimentación |

### Interruptores de Selección de Escenas

| Componente | GPIO | Descripción |
| --- | ---: | --- |
| Botón Escena 1 | 15 | Selecciona escena de círculos |
| Botón Escena 2 | 16 | Selecciona escena de líneas |
| Botón Escena 3 | 17 | Selecciona escena de rectángulos |
| Botón Escena 4 | 18 | Selecciona escena de patrón |

Conecta cada interruptor entre su GPIO y GND. Los pines están configurados con
resistencias PULL_UP internas, por lo que un botón presionado se lee como `0`.

## Organización del proyecto

```text
src/
	boot.py            # Inicialización y bucle principal
	config.py          # Configuración de pines y constantes
	main.py            # Punto de entrada
	lib/
		__init__.py    # Paquete de librería
		animation.py   # Definición de escenas y frames (NUEVO)
		oled_display.py # Driver SSD1306 I2C (NUEVO)
		ssd1306.py     # Driver alternativo (referencia)
tests/
	test_main.py       # Pruebas unitarias
tools/
	upload.sh          # Script para cargar a Pico mediante mpremote
README.md            # Este archivo
requirements.txt     # Dependencias de desarrollo
```

## Descripción de módulos

### `src/config.py`
Centraliza toda la configuración de hardware:
- Pines I2C para la pantalla OLED
- Pines GPIO para los cuatro interruptores
- Constantes de tiempo (frame delay, etc.)
- Parámetros de la pantalla (resolución, dirección I2C)

### `src/boot.py`
Contiene el código principal de la aplicación:
- `init_display()`: Inicializa la pantalla OLED mediante I2C
- `check_scene_selection()`: Verifica cuál interruptor ha sido presionado
- `animate()`: Bucle principal que gestiona la animación

### `src/lib/animation.py`
Define las escenas y frames de animación:
- Clase `AnimationScene`: Representa una escena con múltiples frames
- `scene1_circles()`: Círculos que crecen y encogen
- `scene2_lines()`: Líneas que se desplazan
- `scene3_rectangles()`: Rectángulos que cambian de tamaño
- `scene4_pattern()`: Patrón de tablero de ajedrez parpadeante
- `SCENES`: Lista con las 4 escenas configuradas

### `src/lib/oled_display.py`
Driver para la pantalla OLED SSD1306:
- Clase `OLED_SSD1306`: Gestiona la comunicación I2C y dibujo
- Métodos: `pixel()`, `line()`, `rect()`, `fill()`, `show()`

## Preparar el entorno

Desde la raíz del proyecto:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Ejecutar las pruebas

Las pruebas se ejecutan en el ordenador y no necesitan la Pico conectada:

```bash
source .venv/bin/activate
python -m pytest tests/
```

También se puede comprobar el estilo con:

```bash
ruff check src tests
mypy src tests
```

## Cargar el programa en la Pico

1. Conecta la Raspberry Pi Pico por USB.
2. Cierra la consola `MicroPico vREPL` de VS Code para liberar el puerto serie.
3. Comprueba el nombre del puerto en macOS:

	 ```bash
	 ls /dev/cu.usbmodem*
	 ```

4. Ejecuta el script usando el puerto encontrado. Por ejemplo:

	 ```bash
	 source .venv/bin/activate
	 ./tools/upload.sh /dev/cu.usbmodemXXXX
	 ```

No escribas literalmente `XXXX`: es solo un marcador para el número real del puerto. Si aparece `failed to access ... (it may be in use by another program)`, cierra cualquier terminal serie, REPL o conexión MicroPico que esté usando la Pico y vuelve a ejecutar el comando.

El script copia los archivos de `src/` a la placa mediante `mpremote`. Después de cargar, reinicia la Pico para ejecutar el programa.

## Funcionamiento

1. Al encender la Pico, se ejecuta `main.py` que llama a `boot.animate()`.
2. La pantalla OLED se inicializa a través de I2C.
3. Se muestra la escena por defecto (Escena 1: Círculos Animados).
4. El programa entra en un bucle que:
   - Verifica el estado de los 4 interruptores
   - Si se presiona un botón, cambia a la escena correspondiente
   - Dibuja el frame actual en la pantalla
   - Espera `FRAME_DELAY_MS` (100 ms) antes del siguiente frame
5. Presionando cualquier botón durante la animación cambia inmediatamente a la nueva escena.

## Personalización

### Cambiar velocidad de animación
En `src/config.py`, modifica la constante `FRAME_DELAY_MS`:
```python
FRAME_DELAY_MS = 100  # Aumenta para ir más lento, disminuye para ir más rápido
```

### Agregar nuevas escenas
1. En `src/lib/animation.py`, crea una función `sceneN_description()` similar a las existentes.
2. Crea una lista de frames que llamen a esa función.
3. Agrega una nueva entrada a `SCENES`.
4. Configura más interruptores en `src/config.py` si es necesario.

### Personalizar frames
Cada frame es una función que recibe `(display, frame_num)`.
Usa los métodos de `OLED_SSD1306`:
- `display.fill(0)` o `display.fill(1)`: Limpia o rellena
- `display.pixel(x, y, color)`: Dibuja un píxel
- `display.line(x0, y0, x1, y1, color)`: Dibuja una línea
- `display.rect(x, y, w, h, color)`: Dibuja un rectángulo
- `display.show()`: Actualiza la pantalla

## Notas técnicas

- La pantalla OLED se comunica a 400 kHz (I2C_FREQ = 400_000).
- Cada escena tiene exactamente 12 frames para optimizar la memoria.
- Los botones usan PULL_UP internas (0 = presionado, 1 = no presionado).
- El buffer de la pantalla es de 1024 bytes (128 × 64 / 8).
- Las animaciones son no-bloqueantes: los botones se revisan en cada ciclo.

## Solución de problemas

**Pantalla no muestra nada:**
- Verifica la dirección I2C: intenta 0x3D si 0x3C no funciona.
- Comprueba que SDA y SCL estén correctamente conectados.
- Asegúrate de que la tensión de alimentación sea 3.3V.

**Botones no funcionan:**
- Verifica que estén conectados a los pines correctos.
- Confirma que cada botón está entre GPIO y GND.
- Los pines deben estar configurados con PULL_UP (ya lo están en config.py).

**Animación lenta o entrecortada:**
- Aumenta `FRAME_DELAY_MS` en config.py.
- Verifica que la frecuencia I2C no sea demasiado baja.

