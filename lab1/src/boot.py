import time as t

import src.config as c


def toggle():
    for i in range(len(c.leds)):
        current_state = c.buttons[i].value()
        if current_state == 0 and c.last_state[i] == 1:
            c.leds[i].toggle()
        c.last_state[i] = current_state
    t.sleep(0.02)