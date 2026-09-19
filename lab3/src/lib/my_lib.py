"""Funciones del contador y de la pantalla OLED."""

try:
    import src.config as c
except ImportError:
    import config as c

try:
    from .ssd1306 import SSD1306_I2C
except ImportError:
    try:
        from lib.ssd1306 import SSD1306_I2C
    except ImportError:
        from ssd1306 import SSD1306_I2C

class Pantalla:
    def __init__(self):
        import machine

        self.i2c = machine.I2C(
            1, scl=c.oled_scl, 
            sda=c.oled_sda)
        self.oled = SSD1306_I2C(
            c.oled_width, 
            c.oled_height, 
            self.i2c)

    def start(self):
        self.oled.fill(0)
        self.oled.text("CherryStraw", 0, 0)
        self.oled.text("----------------", 0, 12)
        self.oled.text("Iniciando sistema...", 0, 28)
        self.oled.text("Esto puede tomar", 0, 44)
        self.oled.text("un momento...", 0, 56)
        self.oled.show()
        c.sleep_ms(3000)

    def update_state(self, value, button):
        """Muestra el valor actual y el botón usado."""
        self.oled.fill(0)
        self.oled.text("--- CONTADOR ---", 0, 0)
        self.oled.text(f"Valor: {value}", 0, 24)
        self.oled.text(f"Boton: {button}", 0, 44)
        self.oled.show()


def _write_leds(value):
    """Muestra en los cuatro LEDs los cuatro bits menos significativos."""
    for index, led in enumerate(c.leds):
        led.value((value >> index) & 1)


def count(display=None):
    """Cuenta entre 0 y 100 usando los botones ``up`` y ``down``."""
    while True:
        button = None
        if c.up.value() == 0:
            c.counter = min(c.counter + 1, 100)
            button = "UP"
        elif c.down.value() == 0:
            c.counter = max(c.counter - 1, 0)
            button = "DOWN"

        _write_leds(c.counter)
        if display is not None and button is not None:
            display.update_state(c.counter, button)

        c.sleep_ms(200 if button is not None else 50)