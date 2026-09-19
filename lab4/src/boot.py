"""
Punto de entrada y funciones principales de la aplicación.

Inicializa la pantalla OLED y el controlador de animaciones,
luego ejecuta el bucle principal que gestiona la selección de escenas
y la reproducción de animaciones.
"""

import src.config as c
from src.lib.ssd1306 import OLED_SSD1306
from src.lib.animation import get_scene
from machine import I2C, Pin


def init_display() -> OLED_SSD1306:
    """
    Inicializa la pantalla OLED I2C.
    
    Returns:
        Objeto OLED_SSD1306 configurado y listo
    """
    # Crear objeto I2C con los pines especificados en config
    i2c = I2C(1, scl=Pin(c.I2C_SCL), sda=Pin(c.I2C_SDA), freq=c.I2C_FREQ)
    
    # Inicializar pantalla OLED
    display = OLED_SSD1306(i2c, address=c.OLED_ADDRESS, 
                           width=c.OLED_WIDTH, height=c.OLED_HEIGHT)
    
    return display


def check_scene_selection() -> int:
    """
    Verifica cuál interruptor ha sido presionado.
    
    Retorna el número de escena (0-3) si se presiona un botón,
    o -1 si no se presiona ninguno.
    
    Returns:
        Número de escena (0-3) o -1 si ningún botón presionado
    """
    for i, button in enumerate(c.BUTTONS):
        if button.value() == 0:  # Botón presionado (PULL_UP activo bajo)
            return i
    return -1


def animate() -> None:
    """
    Bucle principal de animación.
    
    Inicializa la pantalla OLED y ejecuta un bucle infinito que:
    1. Verifica la selección de escena mediante los botones
    2. Reproduce la escena seleccionada en un loop
    3. Actualiza la pantalla cada FRAME_DELAY_MS milisegundos
    """
    # Inicializar pantalla
    display = init_display()
    
    # Variable para rastrear la escena actual
    current_scene = c.DEFAULT_SCENE
    frame_index = 0
    
    # Mostrar mensaje inicial
    display.fill(0)
    display.show()
    
    # Bucle principal
    while True:
        # Verificar si se ha seleccionado una nueva escena
        selected = check_scene_selection()
        if selected != -1:
            current_scene = selected
            frame_index = 0
        
        # Obtener la escena actual
        scene = get_scene(current_scene)
        
        # Obtener el frame actual
        frame_func = scene.get_frame(frame_index)
        
        # Dibujar el frame
        try:
            frame_func(display, frame_index)
        except Exception as e:
            # Si hay error en la animación, limpiar pantalla
            display.fill(0)
            display.show()
        
        # Incrementar índice de frame
        frame_index = (frame_index + 1) % scene.frame_count
        
        # Esperar antes del siguiente frame
        c.sleep_ms(c.FRAME_DELAY_MS)

