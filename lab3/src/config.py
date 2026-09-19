"""
Modulo de setup
"""

import time

from machine import Pin as P

# OLED
oled_width = 128
oled_height = 64
oled_sda = 14
oled_scl = 15

# Lista de leds
leds = [
    P(13, P.OUT, P.PULL_UP), 
    P(9, P.OUT, P.PULL_UP), 
    P(18, P.OUT, P.PULL_UP), 
    P(22, P.OUT, P.PULL_UP)
    ]

# Botones de conteo
up = P(16, P.IN, P.PULL_UP)
down = P(17, P.IN, P.PULL_UP)
# GP 11 = Full down
# GP 
# Contador
counter = 0

# Tiempo de espera en milisegundos
sleep_ms = time.sleep_ms

# Tiempo de espera