"""
Configuración centralizada de pines y constantes del proyecto.
Sistema de animación de emociones con OLED y control por botones.
"""

# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN I2C (OLED SSD1306)
# ═══════════════════════════════════════════════════════════════════════════

I2C_SDA = 14
I2C_SCL = 15
I2C_FREQ = 400_000  # 400 kHz
OLED_ADDRESS = 0x3C
OLED_WIDTH = 128
OLED_HEIGHT = 64

# ═══════════════════════════════════════════════════════════════════════════
# BOTONES DE ENTRADA (Pull-Up)
# ═══════════════════════════════════════════════════════════════════════════

BTN_LEFT = 2      # Escena anterior
BTN_RIGHT = 3     # Escena siguiente
BTN_PLAY = 4      # Play/Pause
BTN_RESET = 5     # Reiniciar a escena 0

# ═══════════════════════════════════════════════════════════════════════════
# LEDs DE SALIDA
# ═══════════════════════════════════════════════════════════════════════════

LED_RED = 6       # Error/Reset
LED_GREEN = 7     # Playing indicator
LED_YELLOW = 8    # Scene indicator
LED_BLUE = 9      # System active

# ═══════════════════════════════════════════════════════════════════════════
# PARÁMETROS DE ANIMACIÓN
# ═══════════════════════════════════════════════════════════════════════════

NUM_SCENES = 8
NUM_FRAMES = 12
FRAME_DELAY_MS = 100

# ═══════════════════════════════════════════════════════════════════════════
# ESTADOS DEL SISTEMA
# ═══════════════════════════════════════════════════════════════════════════

STATE_IDLE = 0
STATE_PLAYING = 1
STATE_STOPPED = 2