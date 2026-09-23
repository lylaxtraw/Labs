"""
Sistema de animación con control de escenas y frames.
Gestiona carga de imágenes PBM y reproducción en OLED.
"""

import framebuf
import os
from config import NUM_SCENES, NUM_FRAMES

class PBMAnimation:
    """
    Controlador de animación basado en imágenes PBM.
    Maneja escenas (0-7) y frames (1-12) por escena.
    """
    
    # Nombres de emociones por escena
    EXPRESSION_NAMES = [
        "Feliz",
        "Triste",
        "Enojo",
        "Sorpresa",
        "Miedo",
        "Disgusto",
        "Neutral",
        "Confundido"
    ]
    
    def __init__(self, oled, initial_scene=0):
        """
        Inicializa el sistema de animación.
        
        Args:
            oled: Objeto OLED_SSD1306 inicializado
            initial_scene: Escena inicial (0-7, default: 0)
        """
        self.oled = oled
        self.scene_num = initial_scene
        self.frame_num = 0
        self.is_playing = False
        
        # Construir lista de rutas de frames
        self.frame_paths = self._get_frame_paths(initial_scene)
        
        print(f"PBMAnimation inicializado: Escena {initial_scene} ({self.get_expression_name()})")
    
    def _get_frame_paths(self, scene_num):
        """
        Obtiene lista de rutas de frames para una escena.
        
        Args:
            scene_num: Número de escena (0-7)
            
        Returns:
            Lista de rutas absolutas a frames [1.pbm, 2.pbm, ..., 12.pbm]
        """
        base_path = f"utils/scenes/scene{scene_num}"
        paths = []
        
        for frame_num in range(1, NUM_FRAMES + 1):
            frame_path = f"{base_path}/{frame_num}.pbm"
            paths.append(frame_path)
        
        return paths
    
    def set_scene(self, scene_num):
        """
        Cambia a una nueva escena.
        
        Args:
            scene_num: Número de escena (0-7)
        """
        if scene_num < 0 or scene_num >= NUM_SCENES:
            print(f"Escena inválida: {scene_num}")
            return
        
        self.scene_num = scene_num
        self.frame_num = 0
        self.frame_paths = self._get_frame_paths(scene_num)
        
        # Mostrar primer frame
        self.play_frame(0)
    
    def play_frame(self, frame_num=None):
        """
        Carga y muestra un frame específico.
        
        Args:
            frame_num: Número de frame (0-11, default: frame_num actual)
        """
        if frame_num is not None:
            self.frame_num = frame_num % NUM_FRAMES
        
        frame_path = self.frame_paths[self.frame_num]
        
        try:
            fbuf = self.load_pbm(frame_path)
            if fbuf:
                self.oled.blit(fbuf)
                self.oled.show()
        except Exception as e:
            print(f"Error reproduciendo frame: {e}")
    
    def next_frame(self):
        """Avanza al siguiente frame (con wraparound)."""
        self.frame_num = (self.frame_num + 1) % NUM_FRAMES
        self.play_frame()
    
    def prev_frame(self):
        """Retrocede al frame anterior (con wraparound)."""
        self.frame_num = (self.frame_num - 1) % NUM_FRAMES
        self.play_frame()
    
    def get_expression_name(self):
        """Obtiene nombre de emoción de la escena actual."""
        if 0 <= self.scene_num < len(self.EXPRESSION_NAMES):
            return self.EXPRESSION_NAMES[self.scene_num]
        return "Desconocida"
    
    @staticmethod
    def load_pbm(path):
        """
        Carga imagen PBM P4 (binaria monocromática).
        
        Args:
            path: Ruta al archivo .pbm
            
        Returns:
            FrameBuffer con imagen, o None si hay error
        """
        try:
            with open(path, 'rb') as f:
                # Leer y validar magic number
                magic = f.readline()
                if magic != b'P4\n':
                    print(f"Formato PBM inválido: {magic}")
                    return None
                
                # Saltar líneas de comentario
                while True:
                    pos = f.tell()
                    line = f.readline()
                    if not line.startswith(b'#'):
                        f.seek(pos)
                        break
                
                # Leer dimensiones
                dims_line = f.readline()
                dims_str = dims_line.decode('ascii').strip()
                width, height = map(int, dims_str.split())
                
                # Validar dimensiones
                if width != 128 or height != 64:
                    print(f"Dimensiones inesperadas: {width}x{height}")
                    return None
                
                # Leer exactamente 1024 bytes de datos de píxeles
                pixel_data = f.read(1024)
                
                if len(pixel_data) != 1024:
                    print(f"Datos de píxeles incompletos: {len(pixel_data)} bytes")
                    return None
                
                # Crear FrameBuffer con los datos
                fbuf = framebuf.FrameBuffer(
                    bytearray(pixel_data),
                    width,
                    height,
                    framebuf.MONO_HLSB
                )
                
                return fbuf
        
        except FileNotFoundError:
            print(f"Archivo no encontrado: {path}")
            return None
        except Exception as e:
            print(f"Error cargando PBM {path}: {e}")
            return None
