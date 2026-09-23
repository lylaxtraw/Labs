import time
from config import (
    STATE_IDLE, STATE_PLAYING, STATE_STOPPED,
    NUM_SCENES, NUM_FRAMES,
    FRAME_DELAY_MS,
    BTN_LEFT, BTN_RIGHT, BTN_PLAY, BTN_RESET
)
from utils.animation import PBMAnimation

class AnimationApp:
    """
    Controlador principal de la aplicación de animación.
    Maneja entrada de botones, control de estado y feedback de LEDs.
    """
    
    def __init__(self, oled, buttons, leds):
        """
        Inicializa la aplicación con dispositivos hardware.
        
        Args:
            oled: Objeto de pantalla OLED inicializado
            buttons: Dict con botones {'left', 'right', 'play', 'reset'}
            leds: Dict con LEDs {'red', 'green', 'yellow', 'blue'}
        """
        self.oled = oled
        self.buttons = buttons
        self.leds = leds
        
        # Estado de aplicación
        self.state = STATE_IDLE
        self.scene = 0
        self.frame_delay = FRAME_DELAY_MS / 1000.0  # Convertir a segundos
        
        # Animador
        self.animator = PBMAnimation(oled, self.scene)
        
        # Debouncing de botones
        self.last_button_time = {
            'left': 0,
            'right': 0,
            'play': 0,
            'reset': 0
        }
        self.debounce_ms = 200  # milliseconds
        
        print("Aplicación inicializada")
        print(f"  Escena inicial: {self.scene}")
        print(f"  Estado: IDLE")
        print(f"  Delay frame: {FRAME_DELAY_MS}ms")
    
    def _debounce_check(self, button_name):
        """
        Verifica si ha pasado suficiente tiempo desde la última pulsación.
        
        Args:
            button_name: 'left', 'right', 'play', o 'reset'
            
        Returns:
            True si es seguro procesar este botón (>200ms desde último)
        """
        now_ms = time.ticks_ms()
        last_ms = self.last_button_time[button_name]
        
        if time.ticks_diff(now_ms, last_ms) > self.debounce_ms:
            self.last_button_time[button_name] = now_ms
            return True
        return False
    
    def _update_leds(self):
        """Actualiza estado de LEDs según modo actual."""
        # LED AZUL: Siempre ON cuando sistema activo
        self.leds['blue'].on()
        
        # LED VERDE: ON solo cuando PLAYING
        if self.state == STATE_PLAYING:
            self.leds['green'].on()
        else:
            self.leds['green'].off()
        
        # LED AMARILLO: Indica escena actual
        # Usar brillo relativo (pero GPIO es digital, así que toggle por escena)
        if self.scene % 2 == 0:
            self.leds['yellow'].on()
        else:
            self.leds['yellow'].off()
        
        # LED ROJO: Normalmente OFF (se enciende con RESET)
    
    def _flash_red_led(self, count=3, duration=100):
        """
        Hace parpadear el LED rojo.
        
        Args:
            count: Número de parpadeos
            duration: Duración de cada parpadeo en ms
        """
        for _ in range(count):
            self.leds['red'].on()
            time.sleep(duration / 1000.0)
            self.leds['red'].off()
            time.sleep(duration / 1000.0)
    
    def handle_buttons(self):
        """Lee y procesa pulsaciones de botones."""
        
        # Botón LEFT: Escena anterior
        if not self.buttons['left'].value() and self._debounce_check('left'):
            self.scene = (self.scene - 1) % NUM_SCENES
            self.animator.set_scene(self.scene)
            self.state = STATE_IDLE
            self._update_leds()
            print(f"← Escena {self.scene}: {self.animator.get_expression_name()}")
        
        # Botón RIGHT: Escena siguiente
        if not self.buttons['right'].value() and self._debounce_check('right'):
            self.scene = (self.scene + 1) % NUM_SCENES
            self.animator.set_scene(self.scene)
            self.state = STATE_IDLE
            self._update_leds()
            print(f"→ Escena {self.scene}: {self.animator.get_expression_name()}")
        
        # Botón PLAY: Play/Pause toggle
        if not self.buttons['play'].value() and self._debounce_check('play'):
            if self.state == STATE_PLAYING:
                self.state = STATE_STOPPED
                print("⏸ Pausado")
            else:
                self.state = STATE_PLAYING
                print("▶ Reproduciendo")
            self._update_leds()
        
        # Botón RESET: Reiniciar a escena 0
        if not self.buttons['reset'].value() and self._debounce_check('reset'):
            self.scene = 0
            self.animator.set_scene(0)
            self.state = STATE_IDLE
            print("⟲ Sistema reiniciado - Escena 0")
            self._flash_red_led(2, 100)
            self._update_leds()
    
    def update_animation(self):
        """Actualiza frame de animación si está en modo PLAYING."""
        if self.state == STATE_PLAYING:
            self.animator.next_frame()
            time.sleep(self.frame_delay)
    
    def run_loop(self):
        """Bucle principal de eventos."""
        print("\nIniciando bucle de eventos...")
        print("Pulsa los botones para controlar la animación")
        print("-" * 50)
        
        # Mostrar frame inicial
        try:
            self.animator.play_frame()
            self._update_leds()
        except Exception as e:
            print(f"Error mostrando frame inicial: {e}")
        
        loop_iterations = 0
        
        try:
            while True:
                try:
                    # Procesar botones
                    self.handle_buttons()
                    
                    # Actualizar animación si está playing
                    self.update_animation()
                    
                    # Pequeña pausa para evitar busy-loop
                    time.sleep(0.01)  # 10ms
                    
                    loop_iterations += 1
                    
                except Exception as e:
                    print(f"Error en loop: {e}")
                    # Continuar el loop a pesar del error
                    time.sleep(0.1)
        
        except KeyboardInterrupt:
            print(f"\nDeteniendo... (iteraciones: {loop_iterations})")
            self._shutdown()
        except Exception as e:
            print(f"\nError fatal: {e}")
            self._shutdown()
    
    def _shutdown(self):
        """Apaga todos los LEDs al detener."""
        try:
            self.leds['blue'].off()
            self.leds['green'].off()
            self.leds['yellow'].off()
            self.leds['red'].off()
        except:
            pass
