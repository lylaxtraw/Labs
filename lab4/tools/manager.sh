#!/bin/bash
# Script helper para gestionar animaciones GIF y subir a Pico

set -e

PORT="${PORT:-/dev/cu.usbmodem11101}"
PYTHON="${PYTHON:-python3}"

print_header() {
    echo ""
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║  $1"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo ""
}

print_error() {
    echo "✗ Error: $1" >&2
}

print_success() {
    echo "✓ $1"
}

show_usage() {
    cat << 'EOF'
Sistema de Animación OLED - Gestor de GIFs

Uso:
  ./manager.sh <comando> [opciones]

Comandos:

  convert <gif> <escena>     Convierte GIF a PBM
    Ejemplo: ./manager.sh convert happy.gif 0
    Crea: src/utils/scenes/scene0/*.pbm

  upload-frames              Sube todos los frames al Pico
    Requiere: Pico conectado al puerto $PORT
    Sube: src/utils/scenes/ → Pico:utils/scenes/

  upload-code                Sube código Python al Pico
    Sube: boot.py, config.py, app.py, etc.

  test                       Ejecuta diagnóstico del sistema
    Conecta al Pico y verifica hardware

  run                        Inicia la aplicación en Pico
    Ejecuta: main() en el REPL

  quick <gif> <escena>       Todo en uno: convertir → subir → correr
    Ejemplo: ./manager.sh quick happy.gif 0

Ejemplos:
  # Convertir y subir un GIF
  ./manager.sh convert happy.gif 0
  ./manager.sh upload-frames

  # Subir solo código
  ./manager.sh upload-code

  # Diagnóstico
  ./manager.sh test

  # O todo en uno
  ./manager.sh quick happy.gif 0

EOF
}

cmd_convert() {
    if [ $# -lt 2 ]; then
        print_error "Uso: convert <gif> <escena>"
        echo "  Ejemplo: convert happy.gif 0"
        exit 1
    fi
    
    gif="$1"
    scene="$2"
    
    if [ ! -f "$gif" ]; then
        print_error "Archivo no encontrado: $gif"
        exit 1
    fi
    
    if ! [[ "$scene" =~ ^[0-7]$ ]]; then
        print_error "Escena debe ser 0-7, recibido: $scene"
        exit 1
    fi
    
    print_header "Convertir GIF → PBM (Escena $scene)"
    
    output_dir="src/utils/scenes/scene$scene"
    
    echo "Entrada:   $gif"
    echo "Salida:    $output_dir"
    echo ""
    
    $PYTHON tools/gif_to_pbm.py "$gif" "$output_dir" --resize
    
    print_success "Conversión completada"
}

cmd_upload_frames() {
    print_header "Subir Frames a Pico ($PORT)"
    
    if ! command -v ampy &> /dev/null; then
        print_error "ampy no está instalado. Instala con: pip install adafruit-ampy"
        exit 1
    fi
    
    # Crear directorios
    for scene in {0..7}; do
        ampy --port "$PORT" mkdir "utils/scenes/scene$scene" 2>/dev/null || true
    done
    
    echo "Subiendo frames..."
    total=0
    for scene in {0..7}; do
        for frame in {1..12}; do
            frame_path="src/utils/scenes/scene$scene/$frame.pbm"
            if [ -f "$frame_path" ]; then
                ampy --port "$PORT" put "$frame_path" "utils/scenes/scene$scene/$frame.pbm" 2>/dev/null
                total=$((total + 1))
            fi
        done
    done
    
    echo ""
    print_success "Subidos $total frames"
}

cmd_upload_code() {
    print_header "Subir Código a Pico ($PORT)"
    
    if ! command -v ampy &> /dev/null; then
        print_error "ampy no está instalado. Instala con: pip install adafruit-ampy"
        exit 1
    fi
    
    echo "Creando directorios..."
    ampy --port "$PORT" mkdir lib 2>/dev/null || true
    ampy --port "$PORT" mkdir utils 2>/dev/null || true
    
    echo "Subiendo archivos..."
    
    # Root files
    ampy --port "$PORT" put src/boot.py boot.py
    ampy --port "$PORT" put src/config.py config.py
    ampy --port "$PORT" put src/main.py main.py
    ampy --port "$PORT" put src/app.py app.py
    
    # Lib files
    ampy --port "$PORT" put src/lib/__init__.py lib/__init__.py
    ampy --port "$PORT" put src/lib/ssd1306.py lib/ssd1306.py
    ampy --port "$PORT" put src/lib/sfhm_pantallas.py lib/sfhm_pantallas.py
    
    # Utils files
    ampy --port "$PORT" put src/utils/__init__.py utils/__init__.py
    ampy --port "$PORT" put src/utils/animation.py utils/animation.py
    
    echo ""
    print_success "Código subido"
}

cmd_test() {
    print_header "Ejecutar Diagnóstico"
    
    cat << 'PYEOF' > /tmp/test_pico.py
import sys
import time
import serial

port = '/dev/cu.usbmodem11101'
try:
    with serial.Serial(port, 115200, timeout=0.2) as s:
        s.write(b'\x04')
        s.flush()
        time.sleep(1.5)
        s.write(b'from tests.diagnostic import run_diagnostics\n')
        s.write(b'run_diagnostics()\n')
        s.flush()
        
        time.sleep(15)
        
        captured = bytearray()
        while True:
            data = s.read(4096)
            if not data:
                break
            captured.extend(data)
        
        print(captured.decode('utf-8', errors='replace'))
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
PYEOF
    
    $PYTHON /tmp/test_pico.py
}

cmd_run() {
    print_header "Ejecutar Aplicación"
    
    cat << 'PYEOF' > /tmp/run_app.py
import sys
import time
import serial

port = '/dev/cu.usbmodem11101'
try:
    with serial.Serial(port, 115200, timeout=0.2) as s:
        s.write(b'\x04')
        s.flush()
        time.sleep(1.5)
        s.write(b'from main import main\nmain()\n')
        s.flush()
        
        print("Aplicación ejecutándose. Presiona Ctrl+C para detener...")
        time.sleep(1)
        
        try:
            while True:
                data = s.read(4096)
                if data:
                    print(data.decode('utf-8', errors='replace'), end='')
                time.sleep(0.1)
        except KeyboardInterrupt:
            s.write(b'\x03')
            s.flush()
            print("\n\nAplicación detenida")
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
PYEOF
    
    $PYTHON /tmp/run_app.py
}

cmd_quick() {
    if [ $# -lt 2 ]; then
        print_error "Uso: quick <gif> <escena>"
        exit 1
    fi
    
    gif="$1"
    scene="$2"
    
    cmd_convert "$gif" "$scene"
    cmd_upload_frames
    cmd_run
}

# Main
if [ $# -eq 0 ]; then
    show_usage
    exit 0
fi

command="$1"
shift

case "$command" in
    convert)
        cmd_convert "$@"
        ;;
    upload-frames)
        cmd_upload_frames
        ;;
    upload-code)
        cmd_upload_code
        ;;
    test)
        cmd_test
        ;;
    run)
        cmd_run
        ;;
    quick)
        cmd_quick "$@"
        ;;
    help|-h|--help)
        show_usage
        ;;
    *)
        print_error "Comando desconocido: $command"
        show_usage
        exit 1
        ;;
esac
