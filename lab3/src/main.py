"""Punto de entrada de la aplicación."""

try:
	import src.boot as b
except ImportError:
	import boot as b

pantalla = b.pantalla()
b.count(pantalla)