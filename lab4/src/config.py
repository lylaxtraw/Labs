"""
Configuración de pines y constantes del proyecto.

Define los pines GPIO utilizados para la pantalla OLED y los botones
de selección de escenas.
"""

import time
from machine import Pin, I2C

# Configuración I2C para pantalla OLED
# SDA: GPIO 14, SCL: GPIO 15
I2C_SDA = 14
I2C_SCL = 15
I2C_FREQ = 400_000  # 400 kHz

# Dirección I2C de la pantalla OLED (típicamente 0x3C o 0x3D)
OLED_ADDRESS = 0x3C

# Pines de los interruptores de selección de escenas
# Configurados como entrada con PULL_UP
BUTTON_SCENE_1 = Pin(10, Pin.IN, Pin.PULL_UP)
BUTTON_SCENE_2 = Pin(16, Pin.IN, Pin.PULL_UP)
BUTTON_SCENE_3 = Pin(17, Pin.IN, Pin.PULL_UP)
BUTTON_SCENE_4 = Pin(11, Pin.IN, Pin.PULL_UP)

# Lista de botones para iteración
BUTTONS = [BUTTON_SCENE_1, BUTTON_SCENE_2, BUTTON_SCENE_3, BUTTON_SCENE_4]

# Configuración de tiempo
sleep_ms = time.sleep_ms
sleep_us = time.sleep_us

# Parámetros de la animación
DEFAULT_SCENE = 0  # Escena inicial (0-3)
FRAME_DELAY_MS = 100  # Tiempo entre frames en milisegundos
OLED_WIDTH = 128
OLED_HEIGHT = 64

# Estado de la aplicación
current_scene = DEFAULT_SCENE

# Boton de reinicio
RST = Pin(0, Pin.IN, Pin.PULL_UP)