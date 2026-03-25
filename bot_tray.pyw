"""
Bot Telegram - Lanzador con icono en la bandeja del sistema (System Tray).
Archivo .pyw para que NO se abra ventana de consola.
"""
import threading
import os
import sys
import signal

# Asegurarnos de estar en el directorio correcto
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from PIL import Image
import pystray

# Variable global para el icono
tray_icon = None


def crear_icono():
    """Carga el icono personalizado xrd desde el archivo PNG."""
    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icon_xrd.png')
    if os.path.exists(icon_path):
        img = Image.open(icon_path)
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        return img
    else:
        # Fallback: icono verde con "B" si no existe el archivo
        from PIL import ImageDraw, ImageFont
        size = 64
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse([4, 4, size - 4, size - 4], fill=(46, 204, 113))
        try:
            font = ImageFont.truetype("arial.ttf", 36)
        except Exception:
            font = ImageFont.load_default()
        bbox = draw.textbbox((0, 0), "B", font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        x = (size - text_w) // 2
        y = (size - text_h) // 2 - bbox[1]
        draw.text((x, y), "B", fill='white', font=font)
        return img


def ejecutar_bot():
    """Ejecuta el bot de Telegram en un hilo separado."""
    import bot
    bot.main()


def salir(icon, item):
    """Cierra el bot y el icono del tray de forma forzada."""
    # Detener el icono del tray primero
    icon.stop()
    # Forzar la salida completa del proceso (mata todos los hilos)
    os._exit(0)


def main():
    global tray_icon

    # Iniciar el bot en un hilo secundario (daemon para que muera con el proceso)
    bot_thread = threading.Thread(target=ejecutar_bot, daemon=True)
    bot_thread.start()

    # Crear el menú del tray
    menu = pystray.Menu(
        pystray.MenuItem("Bot Telegram Activo ✅", lambda: None, enabled=False),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Salir", salir)
    )

    # Crear y ejecutar el icono (esto bloquea el hilo principal)
    tray_icon = pystray.Icon(
        name="bot_xrd",
        icon=crear_icono(),
        title="Bot XRD - Control Remoto PC",
        menu=menu
    )

    tray_icon.run()


if __name__ == '__main__':
    main()
