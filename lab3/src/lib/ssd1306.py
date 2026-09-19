"""Controlador mínimo para pantallas SSD1306 I2C en MicroPython."""


class SSD1306_I2C:
	def __init__(self, width, height, i2c, addr=0x3C):
		import framebuf

		self.width = width
		self.height = height
		self.i2c = i2c
		self.addr = addr
		self.buffer = bytearray((height // 8) * width)
		self.framebuf = framebuf.FrameBuffer(
			self.buffer, width, height, framebuf.MONO_VLSB)
		self._write(0x00, b"\xae\xa8" + bytes([height - 1]) + b"\xd3\x00\x40\xa1\xc8\xda\x12\x81\x7f\xa4\xa6\xd5\x80\x8d\x14\xaf")

	def _write(self, control, data):
		self.i2c.writeto(self.addr, bytes([control]) + data)

	def fill(self, color):
		self.framebuf.fill(color)

	def text(self, text, x, y, color=1):
		self.framebuf.text(text, x, y, color)

	def show(self):
		for page in range(self.height // 8):
			self._write(0x00, bytes([0xb0 | page, 0x00, 0x10]))
			start = self.width * page
			self._write(0x40, self.buffer[start:start + self.width])
