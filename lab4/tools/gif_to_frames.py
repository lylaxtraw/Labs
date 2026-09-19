#!/usr/bin/env python3
"""
Convierte GIFs en frames de animación para pantalla OLED SSD1306.

Procesa GIFs de docs/scenes/ y genera módulos Python con funciones
de dibujo optimizadas para pantalla OLED monocromática 128x64.
"""

import sys
import os
from pathlib import Path
from PIL import Image, ImageDraw

# Añadir el directorio padre al path
sys.path.insert(0, str(Path(__file__).parent.parent))


class GIFToFramesConverter:
    """Convierte archivos GIF a frames OLED."""
    
    OLED_WIDTH = 128
    OLED_HEIGHT = 64
    
    def __init__(self):
        """Inicializa el convertidor."""
        self.project_root = Path(__file__).parent.parent
        self.docs_scenes = self.project_root / "docs" / "scenes"
        self.src_lib = self.project_root / "src" / "lib"
    
    def get_gif_files(self):
        """Obtiene lista de GIFs en docs/scenes/."""
        gif_files = []
        for i in range(1, 5):
            scene_path = self.docs_scenes / f"scene_{i}"
            gif_path = list(scene_path.glob("*.gif"))
            if gif_path:
                gif_files.append((i, gif_path[0]))
        return gif_files
    
    def load_gif_frames(self, gif_path):
        """
        Carga todos los frames de un GIF.
        
        Returns:
            Lista de imágenes PIL (frames)
        """
        frames = []
        try:
            gif = Image.open(gif_path)
            for frame_num in range(gif.n_frames):
                gif.seek(frame_num)
                # Convertir a RGB si es necesario
                frame = gif.convert('RGB')
                frames.append(frame)
            return frames
        except Exception as e:
            print(f"Error loading {gif_path}: {e}")
            return []
    
    def frame_to_bw(self, frame):
        """
        Convierte un frame a blanco y negro y lo redimensiona.
        
        Returns:
            Imagen PIL en escala de grises
        """
        # Redimensionar a tamaño OLED
        resized = frame.resize((self.OLED_WIDTH, self.OLED_HEIGHT), Image.Resampling.LANCZOS)
        
        # Convertir a escala de grises
        gray = resized.convert('L')
        
        # Aplicar threshold para obtener imagen binaria
        bw = gray.point(lambda x: 255 if x > 128 else 0, '1')
        
        return bw
    
    def image_to_buffer(self, image):
        """
        Convierte imagen PIL a buffer de bytes para OLED.
        
        El formato es 8 píxeles por byte (vertical), como en SSD1306.
        LSB es el píxel superior.
        
        Returns:
            bytearray de 1024 bytes (128*64/8)
        """
        # Convertir a datos de píxeles binarios
        bw_image = image.convert('1')
        pixels = bw_image.load()
        
        # Rearreglar para formato SSD1306 (8 píxeles por byte, columna por columna)
        buffer = bytearray(self.OLED_WIDTH * self.OLED_HEIGHT // 8)
        
        for x in range(self.OLED_WIDTH):
            for y in range(self.OLED_HEIGHT):
                byte_index = (y // 8) * self.OLED_WIDTH + x
                bit_index = y % 8
                
                # PIL devuelve 0 para negro (apagado) y 255 para blanco (encendido)
                if pixels[x, y] > 128:
                    buffer[byte_index] |= (1 << bit_index)
        
        return buffer
    
    def compress_buffer_rle(self, buffer):
        """
        Comprime buffer usando RLE (Run-Length Encoding).
        
        Formato: [byte, count, byte, count, ...]
        Donde count es la cantidad de repeticiones del byte anterior.
        Rango de count: 1-255
        
        Returns:
            bytearray comprimido
        """
        if not buffer:
            return bytearray()
        
        compressed = bytearray()
        i = 0
        
        while i < len(buffer):
            current_byte = buffer[i]
            count = 1
            
            # Contar repeticiones consecutivas (máximo 255)
            while i + count < len(buffer) and buffer[i + count] == current_byte and count < 255:
                count += 1
            
            compressed.append(current_byte)
            compressed.append(count)
            i += count
        
        return compressed
    
    def decompress_buffer_rle(self, compressed):
        """
        Descomprime buffer RLE.
        
        Args:
            compressed: bytearray comprimido en formato RLE
        
        Returns:
            bytearray descomprimido (1024 bytes)
        """
        decompressed = bytearray()
        i = 0
        
        while i < len(compressed):
            byte_val = compressed[i]
            count = compressed[i + 1]
            
            for _ in range(count):
                decompressed.append(byte_val)
            
            i += 2
        
        return decompressed
    
    def buffer_to_hex_string(self, buffer):
        """Convierte buffer RLE a string hexadecimal."""
        hex_bytes = [f"0x{b:02x}" for b in buffer]
        return ", ".join(hex_bytes)
    
    def generate_frame_function(self, frame_num, buffer, original_size=1024):
        """Genera código Python para una función de frame."""
        # Comprimir buffer
        compressed = self.compress_buffer_rle(buffer)
        compression_ratio = len(compressed) / original_size * 100
        
        # Crear comentario con información del frame
        code = f"    def frame_{frame_num}(display, _=None):\n"
        code += f"        \"\"\"Frame {frame_num}.\"\"\"\n"
        code += f"        # Datos comprimidos RLE (original: {original_size} bytes, comprimido: {len(compressed)} bytes, {compression_ratio:.1f}%)\n"
        code += f"        compressed = bytearray([\n"
        
        # Dividir en líneas de 16 bytes por línea
        for i in range(0, len(compressed), 16):
            chunk = compressed[i:i+16]
            hex_chunk = ", ".join(f"0x{b:02x}" for b in chunk)
            code += f"            {hex_chunk},\n"
        
        code += f"        ])\n"
        code += f"        # Descomprimir RLE\n"
        code += f"        frame_data = bytearray()\n"
        code += f"        for i in range(0, len(compressed), 2):\n"
        code += f"            frame_data.extend([compressed[i]] * compressed[i+1])\n"
        code += f"        display.buffer[:] = frame_data\n"
        code += f"        display.show()\n"
        code += f"\n"
        code += f"    frames.append(frame_{frame_num})\n"
        
        return code
    
    def generate_scene_module(self, scene_num, frames_data):
        """
        Genera módulos Python segmentados para una escena.
        
        Divide los frames en chunks de máximo 8 frames por módulo
        para evitar que MicroPython se quede sin memoria.
        
        Args:
            scene_num: Número de escena (1-4)
            frames_data: Lista de buffers de frames
            
        Returns:
            Lista de tuplas (codigo_python, num_frames_en_parte)
        """
        FRAMES_PER_MODULE = 8
        modules = []
        
        # Segmentar frames
        for chunk_idx, chunk_start in enumerate(range(0, len(frames_data), FRAMES_PER_MODULE)):
            chunk_end = min(chunk_start + FRAMES_PER_MODULE, len(frames_data))
            frames_chunk = frames_data[chunk_start:chunk_end]
            
            code = f'''"""
Animación de escena {scene_num}, parte {chunk_idx + 1}.

Segmento de frames generado desde GIF con compresión RLE.
Total de frames en este segmento: {len(frames_chunk)}
"""


def create_scene{scene_num}_frames_part{chunk_idx}():
    """Crea los frames para la escena {scene_num} (parte {chunk_idx + 1})."""
    frames = []
    
'''
            
            # Generar funciones de frame
            for local_frame_num, buffer in enumerate(frames_chunk):
                code += self.generate_frame_function(local_frame_num, buffer)
            
            code += f"    return frames\n"
            # Retornar tupla con código y número de frames
            modules.append((code, len(frames_chunk)))
        
        return modules
    
    def convert_scene(self, scene_num, gif_path):
        """Convierte una escena completa de GIF a frames segmentados."""
        print(f"Procesando Escena {scene_num}: {gif_path}")
        
        # Cargar frames del GIF
        frames = self.load_gif_frames(gif_path)
        if not frames:
            print(f"  ❌ No se pudieron cargar frames de {gif_path}")
            return False
        
        print(f"  ✓ Cargados {len(frames)} frames")
        
        # Convertir cada frame
        frames_data = []
        for i, frame in enumerate(frames):
            bw_frame = self.frame_to_bw(frame)
            buffer = self.image_to_buffer(bw_frame)
            frames_data.append(buffer)
            if (i + 1) % 20 == 0 or i == len(frames) - 1:
                print(f"  ✓ Convertidos {i+1}/{len(frames)} frames")
        
        # Generar módulos Python segmentados
        modules = self.generate_scene_module(scene_num, frames_data)
        
        # Carpeta destino para los archivos de esta escena
        scene_output_dir = self.docs_scenes / f"scene_{scene_num}"
        
        # Guardar cada módulo en archivo separado
        module_frames_info = []  # Lista de (part_idx, num_frames)
        for part_idx, (module_code, num_frames) in enumerate(modules):
            output_file = scene_output_dir / f"scene_{scene_num}_frames_part{part_idx}.py"
            with open(output_file, 'w') as f:
                f.write(module_code)
            module_frames_info.append((part_idx, num_frames))
            print(f"  ✓ Parte {part_idx + 1}/{len(modules)} guardada: {output_file.name}")
        
        # Generar archivo índice con clase LazyFrameLoader para evitar MemoryError
        # IMPORTANTE: Usar importación dinámica para NO cargar todos los módulos de partes al inicio
        index_code = f'''"""
Índice de frames para escena {scene_num}.

Usa LazyFrameLoader con importación dinámica para cargar frames bajo demanda.
Compatible con MicroPython Raspberry Pi Pico.
"""


def _load_part_lazy(part_idx):
    """Carga un módulo de parte bajo demanda (sin cargar al inicio)."""
    # Usar __import__ para evitar imports globales que carguen todo al inicio
    module_name = f'scene_{scene_num}_frames_part{{part_idx}}'
    create_func_name = f'create_scene{scene_num}_frames_part{{part_idx}}'
    
    try:
        # Intentar importación relativa desde este directorio
        module = __import__(module_name, fromlist=[create_func_name])
        return getattr(module, create_func_name)
    except:
        # Fallback para MicroPython
        import importlib
        module = importlib.import_module(f'.{{module_name}}', package='scenes.scene_{scene_num}')
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
        self._cached_parts = {{}}  # Cache de partes ya cargadas
        self._cached_funcs = {{}}  # Cache de funciones importadas
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
'''
        
        # Agregar información de cada parte (parte_idx, num_frames)
        for part_idx, num_frames_in_part in module_frames_info:
            index_code += f"    ({part_idx}, {num_frames_in_part}),\n"
        
        total_frames = sum(num_frames for _, num_frames in module_frames_info)
        
        index_code += f'''
]

def create_scene{scene_num}_frames():
    """Retorna un LazyFrameLoader para la escena {scene_num} (sin cargar módulos)."""
    return LazyFrameLoader({total_frames}, _LOADERS_INFO)
'''
        
        # Guardar índice en la carpeta de la escena
        index_file = scene_output_dir / f"scene_{scene_num}_frames.py"
        with open(index_file, 'w') as f:
            f.write(index_code)
        print(f"  ✓ Índice guardado: scene_{scene_num}_frames.py")
        
        return True
    
    def run(self):
        """Ejecuta la conversión de todos los GIFs."""
        print("=" * 60)
        print("Convertidor de GIFs a Frames OLED")
        print("=" * 60)
        
        gif_files = self.get_gif_files()
        
        if not gif_files:
            print("❌ No se encontraron archivos GIF en docs/scenes/")
            return False
        
        print(f"\nEncontrados {len(gif_files)} GIF(s)\n")
        
        success_count = 0
        for scene_num, gif_path in gif_files:
            if self.convert_scene(scene_num, gif_path):
                success_count += 1
            print()
        
        print("=" * 60)
        print(f"Conversión completada: {success_count}/{len(gif_files)} escenas")
        print("=" * 60)
        
        return success_count == len(gif_files)


if __name__ == "__main__":
    converter = GIFToFramesConverter()
    success = converter.run()
    sys.exit(0 if success else 1)
