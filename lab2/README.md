# Lab 2: Contador binario con Raspberry Pi Pico

Proyecto de MicroPython para una Raspberry Pi Pico basada en el microcontrolador
RP2040. El circuito utiliza cuatro LEDs para representar un contador de 4 bits,
con valores de `0` a `15`.

- El botón `up` incrementa el contador.
- El botón `down` decrementa el contador.
- El contador vuelve a `0` después de `15` y a `15` antes de `0`.
- Los botones están configurados con resistencia `PULL_UP`, por lo que un botón
	pulsado se lee como `0`.

## Hardware

| Componente | GPIO |
| --- | ---: |
| LED del bit 0, menos significativo | 13 |
| LED del bit 1 | 9 |
| LED del bit 2 | 18 |
| LED del bit 3, más significativo | 22 |
| Botón `up` | 15 |
| Botón `down` | 16 |

Conecta cada LED con su resistencia limitadora de corriente. Conecta cada
botón entre su GPIO y GND. La alimentación debe ser de `3.3 V`.

## Organización del proyecto

```text
src/
	boot.py       # Arranque en la placa
	config.py     # Pines y estado del contador
	main.py       # Punto de entrada
	lib/          # Código auxiliar
tests/          # Pruebas para el ordenador
tools/
	upload.sh     # Carga mediante mpremote
```

## Preparar el entorno

Desde la raíz del proyecto:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Ejecutar las pruebas

Las pruebas se ejecutan en el ordenador y no necesitan la Pico conectada:

```bash
source .venv/bin/activate
python -m pytest tests/
```

También se puede comprobar el estilo con:

```bash
ruff check src tests
```

## Cargar el programa en la Pico

1. Conecta la Raspberry Pi Pico por USB.
2. Cierra la consola `MicroPico vREPL` de VS Code para liberar el puerto serie.
3. Comprueba el nombre del puerto en macOS:

	 ```bash
	 ls /dev/cu.usbmodem*
	 ```

4. Ejecuta el script usando el puerto encontrado. Por ejemplo:

	 ```bash
	 source .venv/bin/activate
	 ./tools/upload.sh /dev/cu.usbmodemXXXX
	 ```

No escribas literalmente `XXXX`: es solo un marcador para el número real del puerto. Si aparece `failed to access ... (it may be in use by another program)`, cierra cualquier terminal serie, REPL o conexión MicroPico que esté usando la Pico y vuelve a ejecutar el comando.

El script copia los archivos de `src/` y `src/lib/` a la placa mediante `mpremote`. Después de cargar, reinicia la Pico para ejecutar el programa.
