"""
Punto de entrada y funciones principales de la aplicación.

Inicializa la pantalla OLED y el controlador de animaciones,
luego ejecuta el bucle principal que gestiona la selección de escenas
y la reproducción de animaciones.
"""

from machine import I2C, Pin

# Imports que funcionan tanto en desarrollo como en Pico
try:
    import config as c
    from lib.animation import get_scene
    from lib.ssd1306 import OLED_SSD1306
except ImportError:
    import sys
    sys.path.insert(0, 'src')
    import config as c
    from lib.animation import get_scene
    from lib.ssd1306 import OLED_SSD1306


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
    print("Iniciando boot.animate()...")
    
    # Inicializar pantalla
    print("Inicializando pantalla OLED...")
    try:
        display = init_display()
        print("✓ Pantalla OLED inicializada")
    except Exception as e:
        print(f"✗ Error al inicializar OLED: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Mostrar pantalla en blanco (verificación de funcionamiento)
    display.fill(0)
    display.show()
    print("✓ Pantalla limpiada")
    
    # Variable para rastrear la escena actual
    current_scene = c.DEFAULT_SCENE
    frame_index = 0
    frame_count = 0
    error_count = 0
    
    print(f"✓ Iniciando con escena {current_scene}")
    print("Bucle principal activo...")
    
    # Bucle principal
    while True:
        try:
            # Verificar si se ha seleccionado una nueva escena
            selected = check_scene_selection()
            if selected != -1:
                current_scene = selected
                frame_index = 0
                print(f"✓ Escena cambiada a {current_scene}")
            
            # Obtener la escena actual
            scene = get_scene(current_scene)
            
            # Obtener el frame actual
            frame_func = scene.get_frame(frame_index)
            
            # Dibujar el frame
            frame_func(display, frame_index)
            display.show()
            
            # Contador de frames exitosos
            frame_count += 1
            if frame_count % 100 == 0:
                print(f"✓ Frames mostrados: {frame_count}, Escena: {current_scene}, Frame: {frame_index}")
            
            # Incrementar índice de frame
            frame_index = (frame_index + 1) % scene.frame_count
            
            # Esperar antes del siguiente frame
            c.sleep_ms(c.FRAME_DELAY_MS)
            
        except Exception as e:
            error_count += 1
            print(f"✗ Error en frame {frame_index}: {e}")
            if error_count > 10:
                print("✗ Demasiados errores, deteniendo...")
                import traceback
                traceback.print_exc()
                return
            
            # Si hay error en la animación, limpiar pantalla
            display.fill(0)
            display.show()
            c.sleep_ms(500)  # Pausa más larga en caso de error

