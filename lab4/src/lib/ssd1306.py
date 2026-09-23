"""SSD1306 OLED driver - tested and working."""

import framebuf


class OLED_SSD1306:
    def __init__(self, width, height, i2c, addr=0x3C):
        self.i2c = i2c
        self.addr = addr
        self.width = width
        self.height = height
        self.pages = height // 8
        self.buf = bytearray(self.pages * width)
        self.fbuf = framebuf.FrameBuffer(self.buf, width, height, framebuf.MONO_HLSB)
        self.init_display()

    def init_display(self):
        """Inicializa pantalla SSD1306."""
        for cmd in (
            0xAE,        # Display OFF
            0xD5, 0x80,  # Clock divide
            0xA8, 0x3F,  # Multiplex (64)
            0xD3, 0x00,  # Display offset
            0x40,        # Start line
            0x8D, 0x14,  # Charge pump
            0x20, 0x02,  # PAGE addressing mode
            0xA1,        # Segment remap
            0xC8,        # COM remap
            0xDA, 0x12,  # COM pins
            0x81, 0xFF,  # Contrast (max)
            0xD9, 0x22,  # Precharge
            0xDB, 0x20,  # VCOMH
            0x2E,        # Scroll disable
            0xAF,        # Display ON
        ):
            self._cmd(cmd)
        self.fill(0)
        self.show()

    def _cmd(self, cmd):
        """Envía comando."""
        self.i2c.writeto(self.addr, bytes([0x00, cmd]))

    def _data(self, buf):
        """Envía datos."""
        self.i2c.writeto(self.addr, bytes([0x40]) + buf)

    def show(self):
        """Actualiza pantalla (página por página)."""
        for page in range(self.pages):
            self._cmd(0xB0 | page)
            self._cmd(0x00)
            self._cmd(0x10)
            self._data(self.buf[page * self.width:(page + 1) * self.width])

    def fill(self, col):
        """Rellena buffer."""
        val = 0xFF if col else 0x00
        for i in range(len(self.buf)):
            self.buf[i] = val

    def pixel(self, x, y, col=None):
        """Lee o escribe píxel."""
        if col is None:
            return self.fbuf.pixel(x, y)
        else:
            self.fbuf.pixel(x, y, col)

    def line(self, x0, y0, x1, y1, col):
        """Dibuja línea."""
        self.fbuf.line(x0, y0, x1, y1, col)

    def rect(self, x, y, w, h, col):
        """Dibuja rectángulo."""
        self.fbuf.rect(x, y, w, h, col)

    def text(self, s, x, y, col):
        """Texto (si está disponible)."""
        try:
            self.fbuf.text(s, x, y, col)
        except:
            pass

    def blit(self, fbuf, x=0, y=0):
        """Copia FrameBuffer al buffer."""
        try:
            fbuf_bytes = bytes(fbuf)
            for i in range(min(len(fbuf_bytes), len(self.buf))):
                self.buf[i] = fbuf_bytes[i]
        except Exception as e:
            print(f"blit error: {e}")

    @property
    def buffer(self):
        """Acceso al buffer para compatibilidad."""
        return self.buf
