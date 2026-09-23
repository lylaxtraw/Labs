"""
Test de animaciones - Verifica que los GIFs convertidos se reproducen en OLED.
Ejecuta desde REPL: from tests.animation_test import test_all_scenes; test_all_scenes()
"""

import time
from boot import init_display
from utils.animation import PBMAnimation

def test_scene_animation(scene_num, duration=5):
    """
    Prueba una escena completa reproduciendo todos sus frames.
    
    Args:
        scene_num: Número de escena (0-3)
        duration: Segundos que se reproduce (default: 5)
    """
    print(f"\n{'='*50}")
    print(f"PRUEBA ESCENA {scene_num}")
    print(f"{'='*50}")
    
    try:
        # Inicializar OLED
        oled = init_display()
        if oled is None:
            print("✗ OLED no inicializado")
            return False
        
        # Crear animador
        print(f"Creando animador para escena {scene_num}...")
        anim = PBMAnimation(oled, scene_num)
        
        # Reproducir frames
        print(f"Reproduciendo animación por {duration} segundos...")
        start = time.time()
        frame_count = 0
        
        while time.time() - start < duration:
            try:
                anim.next_frame()
                frame_count += 1
                time.sleep(0.1)  # 100ms delay
            except Exception as e:
                print(f"  ⚠ Error en frame {frame_count}: {e}")
                time.sleep(0.2)
        
        print(f"✓ Escena {scene_num} reproducida ({frame_count} frames en {duration}s)")
        
        # Limpiar pantalla
        oled.fill(0)
        oled.show()
        
        return True
        
    except Exception as e:
        print(f"✗ Error en escena {scene_num}: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_all_scenes():
    """Prueba todas las 4 escenas con animaciones."""
    
    print("\n")
    print("╔════════════════════════════════════════════════════╗")
    print("║        TEST DE ANIMACIONES - TODAS LAS ESCENAS     ║")
    print("╚════════════════════════════════════════════════════╝")
    
    results = {}
    
    # Prueba escenas 0-3
    for scene in range(4):
        results[scene] = test_scene_animation(scene, duration=3)
        time.sleep(0.5)
    
    # Resumen
    print("\n" + "="*50)
    print("RESUMEN DE PRUEBAS")
    print("="*50)
    
    for scene, passed in results.items():
        status = "✓" if passed else "✗"
        print(f"  {status} Escena {scene}")
    
    total_passed = sum(1 for v in results.values() if v)
    print(f"\nTotal: {total_passed}/4 escenas funcionando")
    
    if total_passed == 4:
        print("\n✓ TODAS LAS ANIMACIONES FUNCIONAN CORRECTAMENTE")
        return True
    else:
        print(f"\n⚠ {4 - total_passed} escena(s) con problemas")
        return False

def test_frame_sequence():
    """Prueba la secuencia de frames específica de una escena."""
    
    print("\n" + "="*50)
    print("PRUEBA DE SECUENCIA DE FRAMES")
    print("="*50)
    
    try:
        oled = init_display()
        anim = PBMAnimation(oled, 0)
        
        print("Probando cada frame de escena 0:")
        print()
        
        for frame_num in range(12):
            try:
                anim.play_frame(frame_num)
                print(f"  ✓ Frame {frame_num + 1}/12 mostrado")
                time.sleep(0.2)
            except Exception as e:
                print(f"  ✗ Frame {frame_num + 1}/12 error: {e}")
        
        # Limpiar
        oled.fill(0)
        oled.show()
        
        print("\n✓ Prueba de secuencia completada")
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def quick_animation_preview():
    """Preview rápido de las 4 animaciones."""
    
    print("\n" + "="*50)
    print("PREVIEW RÁPIDO (1s por escena)")
    print("="*50)
    
    try:
        oled = init_display()
        
        for scene in range(4):
            print(f"\nEscena {scene}...")
            anim = PBMAnimation(oled, scene)
            
            start = time.time()
            frame_count = 0
            
            while time.time() - start < 1.0:
                try:
                    anim.next_frame()
                    frame_count += 1
                    time.sleep(0.1)
                except:
                    pass
            
            print(f"  {frame_count} frames reproducidos")
        
        # Limpiar
        oled.fill(0)
        oled.show()
        
        print("\n✓ Preview completado")
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False
