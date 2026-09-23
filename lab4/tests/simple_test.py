"""
Test rápido de OLED - Diagnóstico simple.
Ejecuta desde REPL: from tests.simple_test import quick_test; quick_test()
"""

import time
from boot import init_display, init_buttons, init_leds

def quick_test():
    """Test rápido sin complicaciones."""
    
    print("\n" + "="*50)
    print("PRUEBA RÁPIDA DE OLED")
    print("="*50 + "\n")
    
    # Paso 1: Inicializar OLED
    print("[1/4] Inicializando OLED...")
    try:
        oled = init_display()
        if oled is None:
            print("  ✗ OLED es None")
            return
        print("  ✓ OLED inicializado")
    except Exception as e:
        print(f"  ✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Paso 2: Llenar blanco
    print("\n[2/4] Llenando pantalla de blanco...")
    try:
        oled.fill(1)
        oled.show()
        print("  ✓ Pantalla blanca (¿ves la OLED blanca?)")
        time.sleep(2)
    except Exception as e:
        print(f"  ✗ Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Paso 3: Llenar negro
    print("\n[3/4] Llenando pantalla de negro...")
    try:
        oled.fill(0)
        oled.show()
        print("  ✓ Pantalla negra (¿ves la OLED negra?)")
        time.sleep(1)
    except Exception as e:
        print(f"  ✗ Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Paso 4: Patrón simple
    print("\n[4/4] Dibujando patrón de prueba...")
    try:
        oled.fill(0)
        # Línea horizontal en el centro
        for x in range(128):
            oled.fbuf.pixel(x, 32, 1)
        # Línea vertical en el centro
        for y in range(64):
            oled.fbuf.pixel(64, y, 1)
        oled.show()
        print("  ✓ Patrón dibujado (¿ves una cruz?)")
        time.sleep(2)
        
        # Limpiar
        oled.fill(0)
        oled.show()
    except Exception as e:
        print(f"  ✗ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*50)
    print("PRUEBA COMPLETADA")
    print("="*50 + "\n")

def test_buttons():
    """Test simple de botones."""
    print("\n" + "="*50)
    print("PRUEBA DE BOTONES (10 segundos)")
    print("="*50 + "\n")
    
    try:
        buttons = init_buttons()
        
        print("Presiona los botones durante 10 segundos...")
        print("  LEFT (pin 2)")
        print("  RIGHT (pin 3)")
        print("  PLAY (pin 4)")
        print("  RESET (pin 5)")
        print()
        
        pressed = {'left': 0, 'right': 0, 'play': 0, 'reset': 0}
        state = {'left': 1, 'right': 1, 'play': 1, 'reset': 1}
        
        start = time.time()
        while time.time() - start < 10:
            for name in ['left', 'right', 'play', 'reset']:
                val = buttons[name].value()
                if state[name] == 1 and val == 0:
                    pressed[name] += 1
                    print(f"  ✓ {name.upper()} pulsado ({pressed[name]}x)")
                state[name] = val
            time.sleep(0.05)
        
        print("\n" + "="*50)
        print("RESUMEN:")
        for name, count in pressed.items():
            status = "✓" if count > 0 else "✗"
            print(f"  {status} {name.upper()}: {count} pulsadas")
        print("="*50 + "\n")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()

def test_all():
    """Ejecutar todo."""
    quick_test()
    test_buttons()
