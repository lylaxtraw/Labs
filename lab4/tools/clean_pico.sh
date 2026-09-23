#!/bin/bash
# Script para limpiar el Pico de archivos innecesarios

PORT="${1:-/dev/cu.usbmodem11101}"

echo "╔════════════════════════════════════════════════════════╗"
echo "║  Limpiando Pico ($PORT)                                ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Función para eliminar archivos
delete_files() {
    local pattern=$1
    echo "Borrando: $pattern"
    mpremote connect "$PORT" exec "
import os
try:
    files = [f for f in os.listdir('.') if f.startswith('$pattern')]
    for f in files:
        os.remove(f)
        print(f'  ✓ {f}')
except Exception as e:
    print(f'  Error: {e}')
"
}

# Función para eliminar directorios recursivamente
delete_tree() {
    local path=$1
    echo "Borrando directorio: $path"
    mpremote connect "$PORT" exec "
import os
import shutil
try:
    if os.path.exists('$path'):
        shutil.rmtree('$path')
        print(f'  ✓ Directorio $path eliminado')
    else:
        print(f'  $path no existe')
except Exception as e:
    print(f'  Error: {e}')
"
}

# Menú interactivo
echo "¿Qué deseas limpiar?"
echo "1) Solo frames (utils/scenes)"
echo "2) Solo código Python"
echo "3) Todo (completa limpieza)"
echo "4) Salir"
echo ""
read -p "Selecciona (1-4): " choice

case $choice in
    1)
        echo ""
        delete_tree "utils/scenes"
        echo ""
        echo "✓ Frames eliminados"
        ;;
    2)
        echo ""
        echo "Borrando código Python..."
        mpremote connect "$PORT" exec "
import os
files_to_delete = ['boot.py', 'config.py', 'main.py', 'app.py']
for f in files_to_delete:
    try:
        os.remove(f)
        print(f'  ✓ {f}')
    except:
        pass
"
        echo ""
        delete_tree "lib"
        delete_tree "utils"
        delete_tree "tests"
        echo ""
        echo "✓ Código eliminado"
        ;;
    3)
        echo ""
        echo "⚠ Eliminaré TODO. Presiona Ctrl+C para cancelar..."
        sleep 2
        
        mpremote connect "$PORT" exec "
import os
import shutil

# Eliminar archivos raíz
root_files = ['boot.py', 'config.py', 'main.py', 'app.py']
for f in root_files:
    try:
        os.remove(f)
        print(f'  ✓ {f}')
    except:
        pass

# Eliminar directorios
dirs = ['lib', 'utils', 'tests']
for d in dirs:
    try:
        if os.path.exists(d):
            shutil.rmtree(d)
            print(f'  ✓ Directorio {d}')
    except:
        pass
"
        echo ""
        echo "✓ Pico limpiado completamente"
        ;;
    4)
        echo "Cancelado"
        exit 0
        ;;
    *)
        echo "Opción inválida"
        exit 1
        ;;
esac

echo ""
echo "Verificando contenido:"
mpremote connect "$PORT" exec "
import os
print('Archivos raíz:', os.listdir('.'))
"
