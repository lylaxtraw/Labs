"""
Módulo de animaciones para pantalla OLED.
Define las cuatro escenas animadas y proporciona funciones para
generar y mostrar frames de animación.
"""

import lib.my_lib as lib

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


# Definir las cuatro escenas de animación
SCENES = [
    AnimationScene("Ojos felices", lib.scene1_frames),
    AnimationScene("Ojos tristes", lib.scene2_frames),
    AnimationScene("Ojos molestos", lib.scene3_frames),
    AnimationScene("Patrón parpadeante", lib.scene4_frames),
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

