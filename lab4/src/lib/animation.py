"""
Módulo de animaciones para pantalla OLED.

Define las cuatro escenas animadas y proporciona funciones para
generar y mostrar frames de animación.
"""


class AnimationScene:
    """Representa una escena de animación con múltiples frames."""
    
    def __init__(self, name: str, frames: list):
        """
        Inicializa una escena de animación.
        
        Args:
            name: Nombre descriptivo de la escena
            frames: Lista de frames (funciones de dibujo)
        """
        self.name = name
        self.frames = frames
        self.frame_count = len(frames)
    
    def get_frame(self, index: int) -> callable:
        """Obtiene un frame específico con índice cíclico."""
        return self.frames[index % self.frame_count]


def create_scene1_frames():
    """Crea los frames para la escena de ojos felices."""
    frames = []
    for frame_num in range(12):
        # Crear una función que captura frame_num
        def make_frame(fn):
            def frame_func(display, _=None):
                display.fill(0)
                
                # Radio que crece y luego encoge (12 frames)
                if fn < 6:
                    radius = 5 + fn * 2
                else:
                    radius = 17 - (fn - 6) * 2
                
                center_x = 64
                center_y = 32
                
                # Dibujar círculo usando aproximación
                for angle in range(0, 360, 30):
                    import math
                    rad = math.radians(angle)
                    x = int(center_x + radius * math.cos(rad))
                    y = int(center_y + radius * math.sin(rad))
                    display.pixel(x, y, 1)
                
                display.show()
            return frame_func
        
        frames.append(make_frame(frame_num))
    
    return frames


def create_scene2_frames():
    """Crea los frames para la escena de ojos tristes."""
    frames = []
    for frame_num in range(12):
        def make_frame(fn):
            def frame_func(display, _=None):
                display.fill(0)
                
                # Líneas horizontales que se desplazan
                line_positions = [10, 20, 30, 40, 50, 60]
                offset = fn * 8
                
                for pos in line_positions:
                    y = (pos + offset) % 64
                    display.line(0, y, 127, y, 1)
                
                # Agregar un rectángulo móvil
                rect_x = (fn * 10) % 128
                display.rect(rect_x, 5, 20, 20, 1)
                
                display.show()
            return frame_func
        
        frames.append(make_frame(frame_num))
    
    return frames


def create_scene3_frames():
    """Crea los frames para la escena de ojos molestos."""
    frames = []
    for frame_num in range(12):
        def make_frame(fn):
            def frame_func(display, _=None):
                display.fill(0)
                
                center_x = 64
                center_y = 32
                
                # Rectángulos de diferentes tamaños
                sizes = [(30, 40), (40, 30), (35, 35), (25, 45), (45, 25), (40, 40)]
                size = sizes[fn % len(sizes)]
                
                x1 = center_x - size[0] // 2
                y1 = center_y - size[1] // 2
                x2 = center_x + size[0] // 2
                y2 = center_y + size[1] // 2
                
                display.rect(x1, y1, x2 - x1, y2 - y1, 1)
                
                # Rectángulos internos concentricos
                margin = 5
                display.rect(x1 + margin, y1 + margin, 
                            x2 - x1 - 2 * margin, y2 - y1 - 2 * margin, 1)
                
                display.show()
            return frame_func
        
        frames.append(make_frame(frame_num))
    
    return frames


def create_scene4_frames():
    """Crea los frames para la escena de ojos ."""
    frames = []
    for frame_num in range(12):
        def make_frame(fn):
            def frame_func(display, _=None):
                display.fill(0)
                
                square_size = 8
                cols = 128 // square_size
                rows = 64 // square_size
                
                # Crear patrón de tablero que cambia con cada frame
                for row in range(rows):
                    for col in range(cols):
                        # Alternar color según paridad y frame
                        if (row + col + fn) % 2 == 0:
                            x = col * square_size
                            y = row * square_size
                            display.rect(x, y, square_size, square_size, 1)
                
                display.show()
            return frame_func
        
        frames.append(make_frame(frame_num))
    
    return frames


# Definir las cuatro escenas de animación
SCENES = [
    AnimationScene("Círculos Animados", create_scene1_frames()),
    AnimationScene("Líneas Dinámicas", create_scene2_frames()),
    AnimationScene("Rectángulos Rotantes", create_scene3_frames()),
    AnimationScene("Patrón Parpadeante", create_scene4_frames()),
]


def get_scene(scene_num: int) -> AnimationScene:
    """
    Obtiene una escena por número (0-3).
    
    Args:
        scene_num: Número de escena (0-3)
    
    Returns:
        Objeto AnimationScene correspondiente
    """
    return SCENES[scene_num % len(SCENES)]

