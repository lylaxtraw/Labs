"""
Módulo de ajustado y set-up
"""

from machine import Pin as P

btns = [15, 14, 16, 17]
leds = [13, 9, 18, 22]

buttons = [P(p, P.IN, P.PULL_UP) for p in btns]
leds = [P(p, P.OUT) for p in leds]

last_state = [1, 1, 1, 1]