import os
import subprocess
from PIL import Image

# Configuración de rutas
IMG_DIR = "img"
OUT_DIR = "escenas"
WIDTH = 128
HEIGHT = 64

def procesar_gifs():
    """Busca GIFs en img/, los convierte a PBM P4 y los organiza en carpetas."""
    if not os.path.exists(IMG_DIR):
        print(f"Error: No se encontró la carpeta '{IMG_DIR}/'. Créala y coloca tus .gif ahí.")
        return False

    if not os.path.exists(OUT_DIR):
        os.makedirs(OUT_DIR)

    gifs = [f for f in os.listdir(IMG_DIR) if f.lower().endswith('.gif')]
    
    if not gifs:
        print(f"No se encontraron archivos .gif en la carpeta '{IMG_DIR}/'.")
        return False

    # Ordenar alfabéticamente para mantener consistencia en las escenas
    gifs.sort()

    for indice, nombre_gif in enumerate(gifs, start=1):
        ruta_gif = os.path.join(IMG_DIR, nombre_gif)
        carpeta_escena = os.path.join(OUT_DIR, str(indice))
        os.makedirs(carpeta_escena, exist_ok=True)
        
        print(f"Procesando [{nombre_gif}] -> Guardando en [{carpeta_escena}/]")
        
        try:
            with Image.open(ruta_gif) as img:
                frame_idx = 1
                while True:
                    # Forzar fondo blanco/negro puro y redimensionar a 128x64 px
                    # .convert('1') transforma la imagen a 1-bit (blanco y negro)
                    frame = img.resize((WIDTH, HEIGHT)).convert('1')
                    
                    nombre_frame = f"frame_{frame_idx}.pbm"
                    ruta_pbm = os.path.join(carpeta_escena, nombre_frame)
                    
                    # Al guardar como .pbm con mode '1', Pillow usa formato P4 (Binario) por defecto
                    frame.save(ruta_pbm)
                    
                    frame_idx += 1
                    try:
                        img.seek(img.tell() + 1)
                    except EOFError:
                        break # Fin de los fotogramas del GIF
        except Exception as e:
            print(f"Error procesando {nombre_gif}: {e}")
            
    return True

def subir_a_pico():
    """Usa mpremote para copiar la carpeta de escenas a la raíz de la Raspberry Pi Pico."""
    print("\nIniciando transferencia a la Raspberry Pi Pico...")
    print("Asegúrate de tener la placa conectada y el puerto serial libre (cierra el monitor serial/MicroPico).")
    
    try:
        # Ejecuta mpremote para copiar la carpeta recursivamente (-r)
        # fs cp -r escenas/ :/escenas
        resultado = subprocess.run(
            ["mpremote", "fs", "cp", "-r", OUT_DIR, f":/{OUT_DIR}"], 
            capture_output=True, 
            text=True
        )
        
        if resultado.returncode == 0:
            print("¡Transferencia completada con éxito!")
        else:
            print("Hubo un problema durante la transferencia:")
            print(resultado.stderr)
            
    except FileNotFoundError:
        print("Error: No se encontró 'mpremote'. Verifica que se instaló correctamente con pip.")

if __name__ == "__main__":
    print("--- Conversor de GIF a PBM P4 para OLED Raspberry Pi Pico ---")
    if procesar_gifs():
        subir_a_pico()