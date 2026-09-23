"""
Script de diagnóstico para la aplicación OLED.
Ejecuta desde el REPL de Pico para verificar hardware y frames.

Uso:
    from tests.diagnostic import run_diagnostics
    run_diagnostics()
"""

import os
import time
from boot import init_display, init_buttons, init_leds
from config import NUM_SCENES, NUM_FRAMES

def check_frames():
    """Verifica que todos los frames estén presentes."""
    print("\n╔═══════════════════════════════════════════════════╗")
    print("║  Verificando frames PBM                           ║")
    print("╚═══════════════════════════════════════════════════╝")
    
    total_frames = 0
    missing = []
    
    for scene in range(NUM_SCENES):
        scene_path = f"utils/scenes/scene{scene}"
        try:
            files = os.listdir(scene_path)
            frame_count = len([f for f in files if f.endswith('.pbm')])
            print(f"  Escena {scene}: {frame_count} frames", end="")
            if frame_count == 12:
                print(" ✓")
                total_frames += frame_count
            else:
                print(f" ✗ (esperado 12)")
                missing.append((scene, frame_count))
        except OSError as e:
            print(f"  Escena {scene}: ✗ {e}")
            missing.append((scene, 0))
    
    print(f"\nTotal: {total_frames}/96 frames")
    return len(missing) == 0

def test_buttons(buttons):
    """Prueba interactiva de botones."""
    print("\n╔═══════════════════════════════════════════════════╗")
    print("║  Prueba de Botones                                ║")
    print("╚═══════════════════════════════════════════════════╝")
    print("Presiona cada botón (10 segundos):")
    print("  LEFT (pin 2)  - Escena anterior")
    print("  RIGHT (pin 3) - Escena siguiente")
    print("  PLAY (pin 4)  - Play/Pause")
    print("  RESET (pin 5) - Reiniciar")
    print()
    
    state = {
        'left': 1,
        'right': 1,
        'play': 1,
        'reset': 1
    }
    
    pressed = {
        'left': False,
        'right': False,
        'play': False,
        'reset': False
    }
    
    start = time.time()
    while time.time() - start < 10:
        # LEFT
        if state['left'] == 1 and buttons['left'].value() == 0:
            pressed['left'] = True
            print("  ✓ LEFT presionado")
        state['left'] = buttons['left'].value()
        
        # RIGHT
        if state['right'] == 1 and buttons['right'].value() == 0:
            pressed['right'] = True
            print("  ✓ RIGHT presionado")
        state['right'] = buttons['right'].value()
        
        # PLAY
        if state['play'] == 1 and buttons['play'].value() == 0:
            pressed['play'] = True
            print("  ✓ PLAY presionado")
        state['play'] = buttons['play'].value()
        
        # RESET
        if state['reset'] == 1 and buttons['reset'].value() == 0:
            pressed['reset'] = True
            print("  ✓ RESET presionado")
        state['reset'] = buttons['reset'].value()
        
        time.sleep(0.05)
    
    detected = sum(1 for v in pressed.values() if v)
    print(f"\nBotones detectados: {detected}/4")
    return detected == 4

def test_leds(leds):
    """Prueba de LEDs."""
    print("\n╔═══════════════════════════════════════════════════╗")
    print("║  Prueba de LEDs                                   ║")
    print("╚═══════════════════════════════════════════════════╝")
    
    led_names = ['red', 'green', 'yellow', 'blue']
    
    for led_name in led_names:
        try:
            led = leds[led_name]
            led.on()
            print(f"  {led_name:<10} ON")
            time.sleep(0.3)
            led.off()
            time.sleep(0.1)
        except Exception as e:
            print(f"  {led_name:<10} ✗ {e}")
    
    print("  ✓ Secuencia completada")

def test_oled(oled):
    """Prueba básica de OLED."""
    print("\n╔═══════════════════════════════════════════════════╗")
    print("║  Prueba de OLED                                   ║")
    print("╚═══════════════════════════════════════════════════╝")
    
    try:
        print("  Intentando llenar de blanco...")
        oled.fill(1)
        oled.show()
        print("  → OLED blanco (mira la pantalla)")
        time.sleep(2)
        
        print("  Intentando llenar de negro...")
        oled.fill(0)
        oled.show()
        print("  → OLED negro (mira la pantalla)")
        time.sleep(1)
        
        # Patrón de prueba simple
        print("  Intentando dibujar patrón...")
        oled.fill(0)  # Negro
        # Dibujar líneas horizontales
        for y in range(0, 64, 8):
            for x in range(128):
                oled.fbuf.pixel(x, y, 1)
        oled.show()
        print("  → Patrón de líneas (mira la pantalla)")
        time.sleep(2)
        
        oled.fill(0)
        oled.show()
        
        print("  ✓ OLED funciona")
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_frame_loading(oled):
    """Prueba cargar un frame específico."""
    print("\n╔═══════════════════════════════════════════════════╗")
    print("║  Prueba de Carga de Frames                        ║")
    print("╚═══════════════════════════════════════════════════╝")
    
    try:
        from utils.animation import PBMAnimation
        
        anim = PBMAnimation(oled, 0)
        
        # Mostrar frame 1
        anim.play_frame(0)
        print("  Frame 1 de escena 0 cargado")
        time.sleep(1)
        
        # Siguiente frame
        anim.next_frame()
        print("  Frame 2 cargado")
        time.sleep(1)
        
        print("  ✓ Frames se cargan correctamente")
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_diagnostics():
    """Ejecuta todas las pruebas de diagnóstico."""
    print("\n")
    print("╔═══════════════════════════════════════════════════╗")
    print("║  DIAGNÓSTICO DEL SISTEMA OLED                    ║")
    print("╚═══════════════════════════════════════════════════╝")
    
    # Inicializar hardware
    print("\nInicializando hardware...")
    oled = init_display()
    buttons = init_buttons()
    leds = init_leds()
    
    if not all([oled, buttons, leds]):
        print("✗ Error al inicializar hardware")
        return
    
    print("✓ Hardware listo")
    
    # Ejecutar pruebas
    results = {}
    
    results['frames'] = check_frames()
    results['oled'] = test_oled(oled)
    results['leds'] = test_leds(leds)
    results['frame_load'] = test_frame_loading(oled)
    results['buttons'] = test_buttons(buttons)
    
    # Resumen
    print("\n╔═══════════════════════════════════════════════════╗")
    print("║  RESUMEN                                          ║")
    print("╚═══════════════════════════════════════════════════╝")
    
    for test_name, passed in results.items():
        status = "✓" if passed else "✗"
        print(f"  {test_name:<20} {status}")
    
    total_passed = sum(1 for v in results.values() if v)
    print(f"\nTotal: {total_passed}/{len(results)} pruebas pasadas")
    
    if total_passed == len(results):
        print("\n✓ Sistema listo para usar")
    else:
        print("\n⚠ Hay problemas que revisar")
