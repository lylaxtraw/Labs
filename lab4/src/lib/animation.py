"""
Módulo de animaciones para pantalla OLED.

Define las cuatro escenas animadas basadas en GIFs convertidos.
Los frames fueron generados automáticamente desde archivos GIF
usando el convertidor gif_to_frames.py.

Los módulos de frames se ubican en docs/scenes/scene_N/
"""

import sys

# Agregar rutas para importar módulos de escenas
# Compatible con MicroPython y desarrollo local
_scene_paths = ['/docs', '/docs/scenes', 'docs', 'docs/scenes', 'src/docs', 'src/docs/scenes']

for _path in _scene_paths:
    if _path not in sys.path:
        sys.path.insert(0, _path)


def _lazy_import_scene_creator(scene_num):
    """Importa dinámicamente la función creadora de una escena."""
    try:
        # Intentar importación relativa desde /docs
        module_name = f'scenes.scene_{scene_num}.scene_{scene_num}_frames'
        create_func_name = f'create_scene{scene_num}_frames'
        
        module = __import__(module_name, fromlist=[create_func_name])
        return getattr(module, create_func_name)
    except ImportError:
        # Fallback: intentar importación desde docs relativo
        try:
            import importlib
            module = importlib.import_module(f'scenes.scene_{scene_num}.scene_{scene_num}_frames')
            return getattr(module, f'create_scene{scene_num}_frames')
        except:
            return None


class AnimationScene:
    """Representa una escena de animación con múltiples frames."""
    
    def __init__(self, name: str, frame_count: int, frames_obj):
        """
        Inicializa una escena de animación.
        
        Args:
            name: Nombre descriptivo de la escena
            frame_count: Número de frames en la escena
            frames_obj: Objeto que actúa como lista con __getitem__ y __len__
        """
        self.name = name
        self.frame_count = frame_count
        self.frames = frames_obj
    
    def get_frame(self, index: int) -> callable:
        """Obtiene un frame específico con índice cíclico."""
        return self.frames[index % self.frame_count]


# Crear escenas bajo demanda (lazy loading a nivel de escena)
_SCENE_CREATORS = [
    ("Escena 1 - Animación desde GIF", 15),
    ("Escena 2 - Animación desde GIF", 101),
    ("Escena 3 - Animación desde GIF", 153),
    ("Escena 4 - Animación desde GIF", 157),
]

_SCENES_CACHE = {}  # Cache para escenas ya cargadas


def _get_scene_object(scene_num: int) -> AnimationScene:
    """Obtiene o crea una escena bajo demanda."""
    if scene_num not in _SCENES_CACHE:
        name, frame_count = _SCENE_CREATORS[scene_num]
        # Importar función creadora dinámicamente
        creator_func = _lazy_import_scene_creator(scene_num + 1)
        if creator_func is None:
            raise ImportError(f"No se pudo importar escena {scene_num + 1}")
        frames_obj = creator_func()  # Esto retorna un LazyFrameLoader del generador
        _SCENES_CACHE[scene_num] = AnimationScene(name, frame_count, frames_obj)
    return _SCENES_CACHE[scene_num]


# Crear proxy SCENES que es compatible con código anterior
class ScenesProxy:
    """Proxy que actúa como lista pero carga escenas bajo demanda."""
    def __getitem__(self, index):
        return _get_scene_object(index)
    
    def __len__(self):
        return 4
    
    def __iter__(self):
        for i in range(4):
            yield _get_scene_object(i)


SCENES = ScenesProxy()



def get_scene(scene_num: int) -> AnimationScene:
    """
    Obtiene una escena específica.
    
    Args:
        scene_num: Número de escena (0-3)
    
    Returns:
        Objeto AnimationScene
    """
    return SCENES[scene_num % len(SCENES)]

