# Práctica: Proyecto de uC interpretando código uPy

**Fecha de desarrollo:** Viernes 28 de Agosto 2026  
**Plataforma:** Raspberry Pi Pico (RP2040)  
**Entorno de desarrollo:** VSCode + MicroPico (intérprete uPy / MicroPython)  
**Integrantes:**

- Estrada Pulido Salvador
- León Díaz Donovan

---

## Material utilizado

- 4 interruptores de pulso (push buttons)
- 4 LEDs
- Cables de conexión (jumpers)
- Microcontrolador: Raspberry Pi Pico (RP2040)
- Entorno de desarrollo: VSCode + MicroPico con soporte para MicroPython (uPy)

---

## Cargado de firmware correspondiente

Para que la Raspberry Pi Pico pueda ejecutar código en MicroPython, es necesario cargar el firmware adecuado (`.uf2`). El procedimiento es el siguiente:

1. **Entrar en modo bootloader:**
   - Mantén presionado el botón **BOOTSEL** de la Pico.
   - Conecta la placa a la computadora mediante un cable USB.
   - Suelta el botón **BOOTSEL** cuando aparezca una unidad de almacenamiento llamada `RPI-RP2`.

2. **Cargar el firmware:**
   - Descarga el archivo `.uf2` más reciente de MicroPython para RP2040 desde [micropython.org/download/RPI_PICO](https://micropython.org/download/RPI_PICO/).
   - Copia y pega el archivo `.uf2` en la unidad `RPI-RP2`.
   - La placa se reiniciará automáticamente y estará lista para ejecutar MicroPython.

3. **Verificar conexión:**
   - En VSCode, con la extensión MicroPico instalada, verifica que aparezca el indicador **"Pico Connected"** en la barra de estado inferior.

---

## Elaboración de código en uPy y su simulación

A continuación se presenta la versión del código original, escrito en Arduino/C++, adaptada a MicroPython (uPy), manteniendo la misma lógica: cada botón controla directamente un LED.

## Código en MicroPython (uPy)

```python
from machine import Pin
import time

# Pines de botones
btn_pins = [15, 14, 16, 17]

# Pines de LEDs
led_pins = [18, 19, 20, 22]

# Configurar pines en PULL_UP
buttons = [Pin(p, Pin.IN, Pin.PULL_UP) for p in btn_pins]
leds = [Pin(p, Pin.OUT, Pin.PULL_UP) for p in led_pins]

# Lista para guardar el estado anterior de cada botón
# Como se usa PULL_UP, el estado normal (sin presionar) es 1
last_state = [1, 1, 1, 1]

# Asegurarnos de que todos los LEDs empiecen apagados
for led in leds:
    led.value(0)

# Bucle principal
while True:
    for i in range(4):
        # Leer el estado actual del botón
        current_state = buttons[i].value()
        
        # Detectar si el botón acaba de ser presionado (pasó de 1 a 0)
        if current_state == 0 and last_state[i] == 1:
            # Alternar (toggle) el estado actual del LED correspondiente
            leds[i].toggle()
            
        # Actualizar el estado del botón para la siguiente lectura
        last_state[i] = current_state
        
    # Pequeña pausa de 20ms para evitar el rebote mecánico (debounce)
    time.sleep(0.02)
```

## Explicación del código

- **Configuración de pines:**
  - Los botones y LEDs se configuran como entradas con resistencia pull-up interna (`Pin.PULL_UP`), lo que significa que su estado normal es `1` (HIGH) y al presionarse cambian a `0` (LOW).
  - Los LEDs se configuran como salidas digitales (`Pin.OUT`).

- **Lógica del bucle:**
  - En cada iteración del `while True`, se lee el estado de cada botón.
  - Si el botón está presionado (`value() == 0`), el LED correspondiente se enciende (`value(1)`).
  - Si el botón no está presionado, el LED se apaga (`value(0)`).

## Simulación

Antes de cargar el código en la placa, puedes:

- Usar el **REPL de MicroPython** en VSCode para probar comandos individuales (por ejemplo, `Pin(18, Pin.OUT).value(1)` para encender un LED).
- Verificar la lógica con un simulador en línea de MicroPython para RP2040 (si está disponible) o mediante pruebas unitarias en el REPL.

---

## Demostración de la práctica

## Montaje físico

1. **Conexión de botones:**
   - Cada botón se conecta entre un pin GPIO (15, 14, 16, 17) y GND.
   - Gracias a la resistencia pull-up interna, no se necesitan resistencias externas.

2. **Conexión de LEDs:**
   - Cada LED se conecta a un pin GPIO (18, 19, 20, 22) a través de una resistencia limitadora de corriente (aprox. 220 Ω) y luego a GND.
   - El ánodo del LED va al pin GPIO y el cátodo a GND (a través de la resistencia).

## Funcionamiento esperado

- Al presionar un botón, el LED correspondiente se enciende inmediatamente.
- Al soltar el botón, el LED se apaga.
- No hay retardo ni debounce implementado, por lo que la respuesta es instantánea (puede haber rebote mecánico en los botones, pero no afecta la funcionalidad básica).

## Prueba en la placa

1. Guarda el código como `main.py` en la placa (o ejecútalo directamente desde VSCode con MicroPico).
2. **Método de carga con MicroPico:** Haz clic en el botón **Run** (icono de play) ubicado en la barra de estado inferior de VSCode para ejecutar el código en la Pico.
3. Al alimentar la placa, el código se ejecutará automáticamente.
4. Presiona cada botón y verifica que el LED correspondiente responda correctamente.

---

## Notas adicionales

- **Debounce (opcional):** Si se observa parpadeo o comportamiento errático en los LEDs al presionar los botones, se puede implementar un pequeño retardo o lógica de debounce en el código.
- **Extensión MicroPico:** Asegúrate de tener instalada la extensión MicroPico en VSCode. Esta extensión proporciona botones en la barra de estado inferior para cargar y ejecutar el código directamente en la Pico.
- **Botón Run de MicroPico:** Para ejecutar el código, utiliza el botón **Run** en la barra de estado inferior de VSCode (no el botón "Run" estándar del editor). Este botón envía el archivo actual a la Pico y lo ejecuta inmediatamente.
- **Documentación oficial:** Consulta la documentación de MicroPython para RP2040 para más ejemplos y detalles sobre la configuración de pines.
