from boot import init_display, init_buttons, init_leds
from app import AnimationApp

def main():
    """
    Punto de entrada principal de la aplicación.
    Inicializa hardware y comienza el bucle de eventos.
    """
    print("╔═══════════════════════════════════════════════════╗")
    print("║       OLED ANIMATION SYSTEM v1.0                 ║")
    print("║    Emoción Facial - MicroPython Pico             ║")
    print("╚═══════════════════════════════════════════════════╝")
    print("")
    
    # Inicializar hardware
    print("Inicializando hardware...")
    try:
        oled = init_display()
        buttons = init_buttons()
        leds = init_leds()
        print("✓ Hardware inicializado correctamente")
        print("")
    except Exception as e:
        print(f"✗ Error al inicializar hardware: {e}")
        return
    
    # Crear aplicación y ejecutar
    print("Iniciando aplicación...")
    app = AnimationApp(oled, buttons, leds)
    
    try:
        app.run_loop()
    except KeyboardInterrupt:
        print("\nAplicación detenida por usuario")
    except Exception as e:
        print(f"\nError en aplicación: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
