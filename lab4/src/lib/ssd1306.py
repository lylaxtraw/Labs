"""
Driver para pantalla OLED SSD1306 sobre I2C.

Proporciona una interfaz simplificada para controlar una pantalla OLED
conectada a través de I2C.
"""

from machine import I2C, Pin


class OLED_SSD1306:
    """
    Driver para pantalla OLED SSD1306 128x64 conectada por I2C.
    """
    
    def __init__(self, i2c: I2C, address: int = 0x3C, 
                 width: int = 128, height: int = 64):
        """
        Inicializa la pantalla OLED.
        
        Args:
            i2c: Objeto I2C configurado
            address: Dirección I2C de la pantalla (por defecto 0x3C)
            width: Ancho de la pantalla en píxeles
            height: Alto de la pantalla en píxeles
        """
        self.i2c = i2c
        self.address = address
        self.width = width
        self.height = height
        self.buffer = bytearray((width * height) // 8)
        
        # Inicializar pantalla
        self._init_display()
    
    def _write_cmd(self, cmd: int) -> None:
        """Envía un comando a la pantalla."""
        self.i2c.writeto(self.address, bytes([0x00, cmd]))
    
    def _write_data(self, data: bytes) -> None:
        """Envía datos a la pantalla."""
        self.i2c.writeto(self.address, bytes([0x40]) + data)
    
    def _init_display(self) -> None:
        """Inicializa la pantalla SSD1306."""
        init_commands = [
            0xAE,  # Display off
            0xD5, 0x80,  # Set clock divide ratio
            0xA8, 0x3F,  # Set multiplex ratio
            0xD3, 0x00,  # Set display offset
            0x40,  # Set start line
            0x8D, 0x14,  # Set charge pump
            0x20, 0x00,  # Set memory addressing mode
            0xA1,  # Set segment re-map
            0xC8,  # Set COM output scan direction
            0xDA, 0x12,  # Set COM pins hardware configuration
            0x81, 0xCF,  # Set contrast control
            0xD9, 0xF1,  # Set pre-charge period
            0xDB, 0x40,  # Set VCOMH
            0x2E,  # Deactivate scroll
            0xAF,  # Display on
        ]
        
        for cmd in init_commands:
            self._write_cmd(cmd)
    
    def fill(self, color: int) -> None:
        """
        Rellena toda la pantalla con un color.
        
        Args:
            color: 0 para negro, 1 para blanco
        """
        fill_byte = 0xFF if color else 0x00
        for i in range(len(self.buffer)):
            self.buffer[i] = fill_byte
    
    def pixel(self, x: int, y: int, color: int) -> None:
        """
        Dibuja un píxel en la pantalla.
        
        Args:
            x: Coordenada X (0-127)
            y: Coordenada Y (0-63)
            color: 0 para negro, 1 para blanco
        """
        if not (0 <= x < self.width and 0 <= y < self.height):
            return
        
        byte_index = (y // 8) * self.width + x
        bit_index = y % 8
        
        if color:
            self.buffer[byte_index] |= (1 << bit_index)
        else:
            self.buffer[byte_index] &= ~(1 << bit_index)
    
    def line(self, x0: int, y0: int, x1: int, y1: int, color: int) -> None:
        """
        Dibuja una línea usando el algoritmo de Bresenham.
        
        Args:
            x0, y0: Punto de inicio
            x1, y1: Punto final
            color: Color del píxel (0 o 1)
        """
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        
        x, y = x0, y0
        while True:
            self.pixel(x, y, color)
            
            if x == x1 and y == y1:
                break
            
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy
    
    def rect(self, x: int, y: int, w: int, h: int, color: int) -> None:
        """
        Dibuja un rectángulo no relleno.
        
        Args:
            x: Coordenada X superior izquierda
            y: Coordenada Y superior izquierda
            w: Ancho del rectángulo
            h: Alto del rectángulo
            color: Color del píxel (0 o 1)
        """
        # Línea superior
        self.line(x, y, x + w - 1, y, color)
        # Línea inferior
        self.line(x, y + h - 1, x + w - 1, y + h - 1, color)
        # Línea izquierda
        self.line(x, y, x, y + h - 1, color)
        # Línea derecha
        self.line(x + w - 1, y, x + w - 1, y + h - 1, color)
    
    def show(self) -> None:
        """Actualiza la pantalla con el contenido del buffer."""
        # Configurar rango de páginas
        self._write_cmd(0x22)
        self._write_cmd(0x00)
        self._write_cmd(0x07)
        
        # Configurar rango de columnas
        self._write_cmd(0x21)
        self._write_cmd(0x00)
        self._write_cmd(0x7F)
        
        # Enviar buffer en bloques
        for page in range(self.height // 8):
            start_index = page * self.width
            end_index = start_index + self.width
            self._write_data(self.buffer[start_index:end_index])
    
    def text(self, x: int, y: int, text: str, color: int = 1) -> None:
        """
        Dibuja texto en la pantalla.
        
        Args:
            x: Coordenada X
            y: Coordenada Y
            text: Texto a mostrar
            color: Color del texto (0 o 1)
        """
        # Implementación simple de texto
        # Esta es una versión básica que dependerá de la disponibilidad de fuentes
        pass
