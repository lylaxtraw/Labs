"""Boot - inicialización de pantalla."""

import config as c
from lib.ssd1306 import OLED_SSD1306
from machine import I2C, Pin


def init_display():
    """Inicializa OLED I2C."""
    try:
        i2c = I2C(1, scl=Pin(c.I2C_SCL), sda=Pin(c.I2C_SDA), freq=c.I2C_FREQ)
        display = OLED_SSD1306(c.OLED_WIDTH, c.OLED_HEIGHT, i2c, c.OLED_ADDRESS)
        print("✓ OLED inicializado")
        return display
    except Exception as e:
        print(f"✗ Error OLED: {e}")
        import traceback
        traceback.print_exc()
        return None


def init_buttons():
    """Inicializa botones con pull-up."""
    try:
        buttons = {
            'left': Pin(c.BTN_LEFT, Pin.IN, Pin.PULL_UP),
            'right': Pin(c.BTN_RIGHT, Pin.IN, Pin.PULL_UP),
            'play': Pin(c.BTN_PLAY, Pin.IN, Pin.PULL_UP),
            'reset': Pin(c.BTN_RESET, Pin.IN, Pin.PULL_UP),
        }
        print("✓ Botones inicializados")
        return buttons
    except Exception as e:
        print(f"✗ Error botones: {e}")
        import traceback
        traceback.print_exc()
        return None


def init_leds():
    """Inicializa LEDs como salidas."""
    try:
        leds = {
            'red': Pin(c.LED_RED, Pin.OUT),
            'green': Pin(c.LED_GREEN, Pin.OUT),
            'yellow': Pin(c.LED_YELLOW, Pin.OUT),
            'blue': Pin(c.LED_BLUE, Pin.OUT),
        }
        # Apagar todos los LEDs al inicio
        for led in leds.values():
            led.off()
        print("✓ LEDs inicializados")
        return leds
    except Exception as e:
        print(f"✗ Error LEDs: {e}")
        import traceback
        traceback.print_exc()
        return None
