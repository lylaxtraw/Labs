#!/bin/bash
PORT="${1:-/dev/cu.usbmodem11101}"

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  Subiendo frames de animación a Pico ($PORT)              ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Crear directorio de escenas
for scene in {0..7}; do
    echo "Subiendo escena $scene..."
    ampy --port "$PORT" mkdir "utils/scenes/scene$scene" 2>/dev/null || true
    
    # Subir frames 1-12
    for frame in {1..12}; do
        frame_path="src/utils/scenes/scene$scene/$frame.pbm"
        if [ -f "$frame_path" ]; then
            ampy --port "$PORT" put "$frame_path" "utils/scenes/scene$scene/$frame.pbm"
        fi
    done
done

echo ""
echo "✓ Frames subidos"
