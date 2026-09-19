import importlib
import sys
from types import SimpleNamespace

import pytest


class StopLoop(Exception):
	"""Detiene el bucle infinito de la aplicación después de una iteración."""


class FakeLed:
	def __init__(self):
		self.values = []

	def value(self, value=None):
		if value is not None:
			self.values.append(value)


class FakeButton:
	def __init__(self, value):
		self.current_value = value

	def value(self):
		return self.current_value


def load_library(monkeypatch, counter, up_value, down_value):
	leds = [FakeLed() for _ in range(4)]
	config = SimpleNamespace(
		leds=leds,
		counter=counter,
		up=FakeButton(up_value),
		down=FakeButton(down_value),
		sleep_ms=lambda _: (_ for _ in ()).throw(StopLoop),
	)
	monkeypatch.setitem(sys.modules, "config", config)

	sys.modules.pop("src.lib.my_lib", None)
	library = importlib.import_module("src.lib.my_lib")
	return importlib.reload(library), config, leds


def test_count_writes_bits_and_increments_when_up_is_pressed(monkeypatch):
	library, config, leds = load_library(monkeypatch, 3, 0, 1)

	with pytest.raises(StopLoop):
		library.count()

	assert [led.values for led in leds] == [[1], [1], [0], [0]]
	assert config.counter == 4


def test_count_decrements_with_wraparound_when_down_is_pressed(monkeypatch):
	library, config, leds = load_library(monkeypatch, 0, 1, 0)

	with pytest.raises(StopLoop):
		library.count()

	assert [led.values for led in leds] == [[0], [0], [0], [0]]
	assert config.counter == 15
