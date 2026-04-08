import os
import subprocess
import time
import sys
import psutil
import tkinter as tk
from tkinter import messagebox

def get_startup_path():
    """Returns the path to the Windows Startup folder for the current user."""
    return os.path.join(os.environ['APPDATA'], r'Microsoft\Windows\Start Menu\Programs\Startup')

def terminate_bot_processes(current_dir):
    """Terminates any pythonw.exe or python.exe processes running bot scripts in this directory."""
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.info.get('cmdline')
            if cmdline:
                cmd_str = " ".join(cmdline).lower()
                # Check if it's a python process running one of our scripts in this directory
                if ("python" in proc.info['name'].lower() and 
                    current_dir.lower() in cmd_str and 
                    ("bot_tray.pyw" in cmd_str or "bot.py" in cmd_str)):
                    print(f"Terminating bot process: {proc.info['pid']}")
                    proc.terminate()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

def run_uninstall():
    # Hide the main tkinter window
    root = tk.Tk()
    root.withdraw()
    
    # Confirm uninstallation
    confirm = messagebox.askyesno(
        "Confirmar Desinstalación", 
        "¿Estás seguro de que quieres eliminar el Bot de Telegram y todos sus archivos del sistema?",
        icon='warning'
    )
    
    if not confirm:
        return

    # El script está en core/, pero queremos borrar la carpeta padre (bot-telegram)
    core_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(core_dir)
    startup_path = get_startup_path()
    shortcut_name = "Bot_xrd.lnk"
    full_shortcut_path = os.path.join(startup_path, shortcut_name)

    print(f"Iniciando desinstalación desde: {project_dir}")

    # 1. Remove the startup shortcut if it exists
    if os.path.exists(full_shortcut_path):
        try:
            os.remove(full_shortcut_path)
            print(f"Acceso directo eliminado: {full_shortcut_path}")
        except Exception as e:
            print(f"Error al eliminar el acceso directo: {e}")

    # 2. Identify and terminate running bot processes
    terminate_bot_processes(project_dir)
    
    # Wait a moment for processes to close
    time.sleep(1)

    # 3. Create a temporary batch file to delete the folder
    # This is necessary because we can't delete the folder while this script is running inside it.
    temp_dir = os.environ.get('TEMP', os.environ.get('TMP', 'C:\\Temp'))
    cleanup_script_path = os.path.join(temp_dir, "bot_uninstall_cleanup.bat")
    
    # We use a batch file that waits, deletes the directory, and then deletes itself.
    with open(cleanup_script_path, "w", encoding='utf-8') as f:
        f.write("@echo off\n")
        f.write("timeout /t 2 /nobreak > nul\n")
        f.write(f'rmdir /s /q "{project_dir}"\n')
        f.write("echo Desinstalación completada con éxito.\n")
        f.write("pause\n")
        f.write("del \"%~f0\"\n")

    # 4. Launch the cleanup script and exit
    try:
        subprocess.Popen(["cmd.exe", "/c", cleanup_script_path], 
                         creationflags=subprocess.CREATE_NEW_CONSOLE)
        print("Script de limpieza lanzado. Saliendo...")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo lanzar el script de limpieza: {e}")
        return

    sys.exit(0)

if __name__ == "__main__":
    run_uninstall()
