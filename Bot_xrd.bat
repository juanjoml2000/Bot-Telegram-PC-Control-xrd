@echo off
chcp 65001 >nul 2>nul

:: Instalar dependencias silenciosamente
pip install -q python-telegram-bot psutil pystray Pillow 2>nul

:: Lanzar el bot con pythonw (sin ventana de consola)
cd /d "C:\Users\Juanjo\Desktop\Trabajo\Proyect\bot-telegram"
start "" pythonw bot_tray.pyw
