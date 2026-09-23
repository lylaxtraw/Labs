cd /Users/salvaxtraw/UV/uP\ y\ uC/Labs/lab4 && \
mpremote connect /dev/cu.usbmodem11101 mkdir lib utils tests && \
for f in src/*.py; do mpremote connect /dev/cu.usbmodem11101 cp "$f" ":$(basename $f)"; done && \
for f in src/lib/*.py; do mpremote connect /dev/cu.usbmodem11101 cp "$f" ":lib/$(basename $f)"; done && \
for f in src/utils/*.py; do mpremote connect /dev/cu.usbmodem11101 cp "$f" ":utils/$(basename $f)"; done && \
for f in tests/*.py; do mpremote connect /dev/cu.usbmodem11101 cp "$f" ":tests/$(basename $f)"; done && \
echo "✓ Todo subido"cd /Users/salvaxtraw/UV/uP\ y\ uC/Labs/lab4 && \
mpremote connect /dev/cu.usbmodem11101 mkdir lib utils tests && \
for f in src/*.py; do mpremote connect /dev/cu.usbmodem11101 cp "$f" ":$(basename $f)"; done && \
for f in src/lib/*.py; do mpremote connect /dev/cu.usbmodem11101 cp "$f" ":lib/$(basename $f)"; done && \
for f in src/utils/*.py; do mpremote connect /dev/cu.usbmodem11101 cp "$f" ":utils/$(basename $f)"; done && \
for f in tests/*.py; do mpremote connect /dev/cu.usbmodem11101 cp "$f" ":tests/$(basename $f)"; done && \
echo "✓ Todo subido"#!/bin/bash
PORT="${1:-/dev/cu.usbmodem11101}"

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  Subiendo archivos a Pico ($PORT)                         ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

echo "Creando directorios..."
ampy --port "$PORT" mkdir lib 2>/dev/null || true
ampy --port "$PORT" mkdir utils 2>/dev/null || true

echo "Subiendo archivos raíz..."
ampy --port "$PORT" put src/boot.py boot.py
ampy --port "$PORT" put src/config.py config.py
ampy --port "$PORT" put src/main.py main.py
ampy --port "$PORT" put src/app.py app.py

echo "Subiendo librerías..."
ampy --port "$PORT" put src/lib/__init__.py lib/__init__.py
ampy --port "$PORT" put src/lib/ssd1306.py lib/ssd1306.py
ampy --port "$PORT" put src/lib/sfhm_pantallas.py lib/sfhm_pantallas.py

echo "Subiendo utils..."
ampy --port "$PORT" put src/utils/__init__.py utils/__init__.py
ampy --port "$PORT" put src/utils/animation.py utils/animation.py

echo ""
echo "✓ Archivos subidos"
