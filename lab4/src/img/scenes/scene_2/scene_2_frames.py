"""
Índice de frames para escena 2.

Usa LazyFrameLoader con importación dinámica para cargar frames bajo demanda.
Compatible con MicroPython Raspberry Pi Pico.
"""


def _load_part_lazy(part_idx):
    """Carga un módulo de parte bajo demanda (sin cargar al inicio)."""
    # Usar __import__ para evitar imports globales que carguen todo al inicio
    module_name = f'scene_2_frames_part{part_idx}'
    create_func_name = f'create_scene2_frames_part{part_idx}'
    
    try:
        # Intentar importación relativa desde este directorio
        module = __import__(module_name, fromlist=[create_func_name])
        return getattr(module, create_func_name)
    except:
        # Fallback para MicroPython
        import importlib
        module = importlib.import_module(f'.{module_name}', package='scenes.scene_2')
        return getattr(module, create_func_name)


class LazyFrameLoader:
    """Carga frames bajo demanda sin almacenarlos todos en memoria."""
    
    def __init__(self, num_frames, loaders_info):
        """
        Inicializa el cargador lazy.
        
        Args:
            num_frames: Número total de frames
            loaders_info: Lista de tuplas (part_idx, num_frames_en_parte)
        """
        self.num_frames = num_frames
        self.loaders_info = loaders_info  # [(0, 8), (1, 8), ...]
        self._cached_parts = {}  # Cache de partes ya cargadas
        self._cached_funcs = {}  # Cache de funciones importadas
        self._frame_to_part = []  # Mapeo de frame_index -> (part_idx, local_idx)
        
        # Construir mapeo de frame a parte
        frame_idx = 0
        for part_idx, num_in_part in loaders_info:
            for local_idx in range(num_in_part):
                self._frame_to_part.append((part_idx, local_idx))
                frame_idx += 1
    
    def __getitem__(self, index):
        """Obtiene un frame específico."""
        index = index % self.num_frames
        part_idx, local_idx = self._frame_to_part[index]
        
        # Cargar la parte si no está en cache
        if part_idx not in self._cached_parts:
            # Importar función si no está en cache (PRIMER ACCESO)
            if part_idx not in self._cached_funcs:
                self._cached_funcs[part_idx] = _load_part_lazy(part_idx)
            
            # Ejecutar función para obtener frames
            create_func = self._cached_funcs[part_idx]
            frames = create_func()
            self._cached_parts[part_idx] = frames
        
        return self._cached_parts[part_idx][local_idx]
    
    def __len__(self):
        """Retorna el número de frames."""
        return self.num_frames


# Definir loaders sin cargar módulos - solo información sobre dónde están
_LOADERS_INFO = [
    (0, 8),
    (1, 8),
    (2, 8),
    (3, 8),
    (4, 8),
    (5, 8),
    (6, 8),
    (7, 8),
    (8, 8),
    (9, 8),
    (10, 8),
    (11, 8),
    (12, 5),

]

def create_scene2_frames():
    """Retorna un LazyFrameLoader para la escena 2 (sin cargar módulos)."""
    return LazyFrameLoader(101, _LOADERS_INFO)
