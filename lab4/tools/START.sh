#!/bin/bash
# Quick start - Inicio rápido del sistema OLED

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  SISTEMA OLED - ANIMACIONES EMOTICON                      ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Detectar Pico
if [ ! -c /dev/cu.usbmodem11101 ]; then
    echo "⚠ Pico no detectado en /dev/cu.usbmodem11101"
    echo ""
    echo "Paso 1: Conecta el Pico por USB"
    echo "Paso 2: Ejecuta de nuevo este script"
    exit 1
fi

echo "✓ Pico detectado"
echo ""
echo "Opciones:"
echo ""
echo "  1. Diagnóstico del sistema"
echo "     bash manager.sh test"
echo ""
echo "  2. Convertir GIF a animación"
echo "     bash manager.sh convert <archivo.gif> <escena(0-7)>"
echo "     Ejemplo: bash manager.sh convert happy.gif 0"
echo ""
echo "  3. Subir frames al Pico"
echo "     bash manager.sh upload-frames"
echo ""
echo "  4. Ejecutar aplicación"
echo "     bash manager.sh run"
echo ""
echo "  5. Todo en uno (convertir + subir + ejecutar)"
echo "     bash manager.sh quick <archivo.gif> <escena(0-7)>"
echo ""
echo "Para más información:"
echo "  cat SETUP_GUIDE.md"
echo "  bash manager.sh help"
echo ""
