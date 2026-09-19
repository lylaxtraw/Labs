"""Funciones de la aplicación."""

import src.config as c


def count():
    while True:
        for bit, led in enumerate(c.leds):
            led.value((c.counter >> bit) & 1)

        if c.up.value() == 0:
            c.counter = (c.counter + 1) % 16

        elif c.down.value() == 0:
            c.counter = (c.counter - 1) % 16

        c.sleep_ms(500)