## Estructura del Proyecto - Lab 4: Animación OLED

### Organización de Carpetas (Estándar MicroPython)

```
Lab 4/
├── README.md                  # Documentación completa
├── requirements.txt           # Dependencias (ruff, mypy, pytest, mpremote)
│
├── docs/                      # Documentación de referencia
│   ├── Guía labs.pdf         # (original)
│   ├── LAB_02.pdf            # (original - referencia estructura)
│   └── archivos_tipicos.pdf  # (original - referencia estructura)
│
├── src/                       # Código principal PRINCIPAL
│   ├── __init__.py           # Paquete principal
│   ├── main.py               # Punto de entrada (llama a boot.animate())
│   ├── boot.py               # Inicialización y bucle principal
│   ├── config.py             # Configuración centralizada de pines
│   │
│   └── lib/                  # Módulos auxiliares reutilizables
│       ├── __init__.py       # Paquete de librería
│       ├── animation.py      # Definición de escenas y frames
│       ├── ssd1306.py        # Driver OLED SSD1306 (PRINCIPAL)
│       ├── oled_display.py   # Referencia histórica (No usar - ver ssd1306.py)
│       └── my_lib.py         # Residual Lab 2 (No usar)
│
├── tests/                     # Pruebas unitarias
│   └── test_main.py          # 12 tests para animaciones
│
├── tools/                     # Herramientas
│   └── upload.sh             # Script para cargar a Raspberry Pi Pico
│
└── .venv/                    # Entorno virtual Python (generado)
```

### Archivos Principales y su Propósito

#### `src/config.py`
- Centraliza configuración de hardware
- Define pines I2C (SDA=4, SCL=5)
- Define pines de botones (GPIO 15-18)
- Constantes de tiempo y pantalla
- Estado global de la aplicación

#### `src/boot.py`
- `init_display()`: Inicializa pantalla OLED
- `check_scene_selection()`: Lee estado de botones
- `animate()`: Bucle principal de animación

#### `src/lib/animation.py`
- Clase `AnimationScene`: Encapsula escenas con frames
- `create_scene*_frames()`: Generadores de frames
- `SCENES`: Lista de 4 escenas
- `get_scene()`: Acceso indexado a escenas

#### `src/lib/ssd1306.py` (DRIVER PRINCIPAL)
- Clase `OLED_SSD1306`: Driver I2C para pantalla
- Métodos: `fill()`, `pixel()`, `line()`, `rect()`, `show()`
- Gestión de buffer de 1024 bytes (128×64/8)

### Archivos Históricos/Referencia (No usar)
- `src/lib/oled_display.py`: Versión anterior del driver (contenido en ssd1306.py)
- `src/lib/my_lib.py`: Funciones del Lab 2 (no aplicables a Lab 4)

### Estructura de Importaciones

```python
# En boot.py:
import src.config as c                    # Configuración
from src.lib.ssd1306 import OLED_SSD1306  # Driver OLED (PRINCIPAL)
from src.lib.animation import get_scene   # Escenas de animación

# En main.py:
import src.boot as b
b.animate()  # Inicia el sistema
```

### Convenciones Aplicadas

1. **Separación de responsabilidades**
   - `config.py`: Configuración centralizada
   - `boot.py`: Lógica de aplicación
   - `lib/`: Módulos reutilizables

2. **Nomenclatura de módulos**
   - Nombres descriptivos en minúsculas
   - Clases en PascalCase (OLED_SSD1306)
   - Funciones en snake_case

3. **Documentación**
   - Docstrings en todas las funciones
   - Comentarios explicativos en puntos complejos
   - README detallado con instrucciones

4. **Independencia de plataforma**
   - `config.py` permite cambiar pines fácilmente
   - Drivers encapsulados en módulos
   - Código portable a otros uC MicroPython

### Pruebas

Archivo: `tests/test_main.py`
- 12 tests unitarios pasando ✓
- Verifican estructura y contenido de escenas
- No requieren hardware

Ejecutar:
```bash
pytest tests/test_main.py -v
```

### Validación Final

✓ Estructura estándar MicroPython aplicada
✓ Archivos residuales documentados y separados
✓ Driver OLED en ssd1306.py (estándar)
✓ 4 escenas animadas con 12 frames cada una
✓ Selección de escenas con interruptores
✓ Todas las pruebas unitarias pasando
✓ README completo con instrucciones
