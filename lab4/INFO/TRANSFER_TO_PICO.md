# Transferir Proyecto a Raspberry Pi Pico

## ✅ Estado Actual: Listo para Transferencia

- **Tamaño total**: 0.98 MB (cabe perfectamente)
- **Espacio en Pico**: ~1.9 MB disponible
- **rshell**: Ya instalado en tu sistema

## 🚀 Pasos Rápidos

```bash
# 1. Conecta Pico al USB

# 2. Abre rshell
$ rshell

# 3. Dentro de rshell:
> cp -r src/* /pyboard/

# 4. Verifica:
> ls /pyboard/
# Deberías ver: boot.py, config.py, docs/, lib/, main.py

# 5. Sal:
> exit
```

**¡Listo!** La Pico ejecutará automáticamente `main.py`.

## 📋 Contenido que se Copia

```
src/
├── main.py              Punto de entrada (ejecutado automáticamente)
├── boot.py              Inicialización OLED
├── config.py            Configuración de pines
├── lib/                 Módulos (animation, ssd1306)
└── docs/scenes/         4 escenas con 426 frames (975 KB)
                         Total: 0.98 MB
```

## ❓ Solución de Problemas

**"no module named 'lib'"**
- Verifica: `> ls /pyboard/` debe mostrar `lib/`

**Nada en la OLED**
- Revisa conexión I2C (GPIO 14 SDA, GPIO 15 SCL)
- Revisa INFO/README_PICO.md para hardware

**Transferencia lenta**
- Normal la primera vez. Las siguientes son más rápidas.

## 📚 Documentación Completa

- `INFO/TRANSFER_TO_PICO.md` - Esta guía (pasos completos)
- `INFO/README_PICO.md` - Detalles de hardware
- `INFO/RESUMEN_FINAL.md` - Resumen técnico
- `INFO/INSTALLATION_GUIDE.md` - Instalación paso a paso

## 🔄 Para Regenerar Animaciones

```bash
# 1. Coloca .gif en tools/gifs/
# 2. Genera:
$ python3 tools/gif_to_frames.py

# 3. Copia a Pico:
$ rshell
> cp -r src/* /pyboard/
> exit
```

---

**Última actualización**: 2025-09-19
