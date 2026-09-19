"""
Script de diagnóstico para probar OLED en Pico.
Ejecutar en la Pico para diagnosticar problemas.

Pasos:
1. Copia este archivo a main.py en la Pico
2. Mira la salida en el REPL
"""

import time
from machine import I2C, Pin

print("=" * 50)
print("DIAGNÓSTICO OLED RASPBERRY PI PICO")
print("=" * 50)

# Paso 1: Verificar pines
print("\n[1/5] Probando pines GPIO...")
try:
    sda_pin = Pin(14, Pin.IN)
    scl_pin = Pin(15, Pin.IN)
    print("  ✓ Pines SDA (14) y SCL (15) accesibles")
except Exception as e:
    print(f"  ✗ Error en pines: {e}")
    exit()

# Paso 2: Inicializar I2C
print("\n[2/5] Inicializando I2C...")
try:
    i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400_000)
    print("  ✓ I2C inicializado en frecuencia 400kHz")
except Exception as e:
    print(f"  ✗ Error en I2C: {e}")
    exit()

# Paso 3: Escanear dispositivos I2C
print("\n[3/5] Escaneando dispositivos I2C...")
try:
    devices = i2c.scan()
    if devices:
        print(f"  ✓ Dispositivos encontrados: {[hex(d) for d in devices]}")
        if 0x3C in devices:
            print("  ✓ Pantalla OLED en 0x3C detectada!")
        elif 0x3D in devices:
            print("  ✓ Pantalla OLED en 0x3D detectada!")
        else:
            print("  ⚠ Pantalla no está en 0x3C ni 0x3D")
    else:
        print("  ✗ NO se detectó ningún dispositivo I2C")
        print("  Verifica conexión SDA (GPIO14) y SCL (GPIO15)")
        exit()
except Exception as e:
    print(f"  ✗ Error al escanear: {e}")
    exit()

# Paso 4: Intentar inicializar OLED
print("\n[4/5] Inicializando pantalla SSD1306...")
try:
    from src.lib.ssd1306 import OLED_SSD1306
    print("  ✓ Módulo ssd1306 importado")
    
    oled = OLED_SSD1306(i2c, address=0x3C, width=128, height=64)
    print("  ✓ Objeto OLED_SSD1306 creado")
    
    # Limpiar pantalla
    oled.fill(0)
    oled.show()
    print("  ✓ Pantalla limpiada")
except Exception as e:
    print(f"  ✗ Error al inicializar OLED: {e}")
    import traceback
    traceback.print_exc()
    exit()

# Paso 5: Dibujar patrón de prueba
print("\n[5/5] Dibujando patrón de prueba...")
try:
    # Dibujar línea horizontal
    for x in range(0, 128, 2):
        oled.pixel(x, 32, 1)
    oled.show()
    print("  ✓ Línea horizontal dibujada")
    time.sleep(1)
    
    # Dibujar línea vertical
    oled.fill(0)
    for y in range(0, 64, 2):
        oled.pixel(64, y, 1)
    oled.show()
    print("  ✓ Línea vertical dibujada")
    time.sleep(1)
    
    # Llenar pantalla
    oled.fill(1)
    oled.show()
    print("  ✓ Pantalla completamente blanca")
    time.sleep(1)
    
    # Limpiar
    oled.fill(0)
    oled.show()
    print("  ✓ Pantalla limpiada")
    
except Exception as e:
    print(f"  ✗ Error al dibujar: {e}")
    import traceback
    traceback.print_exc()
    exit()

print("\n" + "=" * 50)
print("✓ OLED FUNCIONANDO CORRECTAMENTE")
print("=" * 50)
print("\nAhora probando animaciones...")
print("Importando módulo de animación...")

try:
    import sys
    sys.path.insert(0, '/docs')
    from scenes.scene_1.scene_1_frames import create_scene1_frames
    print("✓ Scene 1 importada correctamente")
    
    loader = create_scene1_frames()
    print(f"✓ LazyFrameLoader creado: {loader.num_frames} frames")
    
    # Obtener primer frame
    frame_func = loader[0]
    print(f"✓ Frame 0 obtenido: {type(frame_func).__name__}")
    
    # Dibujar frame
    print("Dibujando frame 0 en OLED...")
    frame_func(oled, 0)
    oled.show()
    print("✓ Frame dibujado en OLED")
    
except Exception as e:
    print(f"✗ Error con animación: {e}")
    import traceback
    traceback.print_exc()

print("\n✓ DIAGNÓSTICO COMPLETADO")
