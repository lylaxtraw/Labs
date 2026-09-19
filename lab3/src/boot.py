"""Funciones de arranque de la aplicación."""

try:
	from src.lib.my_lib import Pantalla
	from src.lib.my_lib import count as _count
except ImportError:
	from lib.my_lib import Pantalla
	from lib.my_lib import count as _count


def count(display=None):
	"""Ejecuta el bucle principal del contador."""
	_count(display)


def pantalla():
	"""Inicializa la pantalla OLED y muestra el mensaje de inicio."""
	display = Pantalla()
	display.start()
	return display