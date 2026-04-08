import os
import sys
import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess

# Estética Premium
COLORS = {
    "bg": "#1e1e2e",
    "fg": "#cdd6f4",
    "accent": "#89b4fa",
    "secondary": "#313244",
    "success": "#a6e3a1",
    "error": "#f38ba8"
}

class SetupApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bot XRD - Instalador y Configurador")
        self.root.geometry("700x850")
        self.root.configure(bg=COLORS["bg"])

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TFrame", background=COLORS["bg"])
        self.style.configure("TLabel", background=COLORS["bg"], foreground=COLORS["fg"], font=("Segoe UI", 10))
        self.style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"), foreground=COLORS["accent"])
        self.style.configure("TEntry", fieldbackground=COLORS["secondary"], foreground=COLORS["fg"])
        self.style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"))

        self.main_container = ttk.Frame(root, padding="20")
        self.main_container.pack(fill="both", expand=True)

        self.create_widgets()
        self.load_data()

    def create_section_header(self, parent, text):
        lbl = ttk.Label(parent, text=text, style="Header.TLabel")
        lbl.pack(pady=(15, 5), anchor="w")
        ttk.Separator(parent, orient="horizontal").pack(fill="x", pady=5)

    def create_field(self, parent, label_text, var_name):
        frame = ttk.Frame(parent)
        frame.pack(fill="x", pady=2)
        ttk.Label(frame, text=label_text, width=20).pack(side="left")
        entry = ttk.Entry(frame)
        entry.pack(side="left", fill="x", expand=True)
        setattr(self, f"entry_{var_name}", entry)
        return entry

    def create_widgets(self):
        # Título
        title = ttk.Label(self.main_container, text="CONFIGURACIÓN DEL BOT XRD", style="Header.TLabel")
        title.pack(pady=(0, 20))

        # Sección 1: Telegram
        self.create_section_header(self.main_container, "1. Credenciales de Telegram")
        self.create_field(self.main_container, "Token de Bot:", "token")
        self.create_field(self.main_container, "Tu ID de Admin:", "admin_id")

        # Sección 2: Juegos
        self.create_section_header(self.main_container, "2. Configuración de Juegos (Steam)")
        
        for i in range(1, 3):
            lbl = ttk.Label(self.main_container, text=f"Juego {i}:", font=("Segoe UI", 10, "bold"))
            lbl.pack(pady=(5, 0), anchor="w")
            f_game = ttk.Frame(self.main_container)
            f_game.pack(fill="x")
            
            ttk.Label(f_game, text="Nombre:").grid(row=0, column=0, padx=5)
            setattr(self, f"game_name_{i}", ttk.Entry(f_game))
            getattr(self, f"game_name_{i}").grid(row=0, column=1, sticky="ew", padx=2)
            
            ttk.Label(f_game, text="Steam ID:").grid(row=0, column=2, padx=5)
            setattr(self, f"game_sid_{i}", ttk.Entry(f_game, width=10))
            getattr(self, f"game_sid_{i}").grid(row=0, column=3, sticky="ew", padx=2)
            
            ttk.Label(f_game, text="Proceso .exe:").grid(row=0, column=4, padx=5)
            setattr(self, f"game_proc_{i}", ttk.Entry(f_game))
            getattr(self, f"game_proc_{i}").grid(row=0, column=5, sticky="ew", padx=2)
            f_game.columnconfigure((1, 3, 5), weight=1)

        # Sección 3: Aplicaciones
        self.create_section_header(self.main_container, "3. Configuración de Aplicaciones")
        
        for i in range(1, 4):
            lbl = ttk.Label(self.main_container, text=f"Aplicación {i}:", font=("Segoe UI", 10, "bold"))
            lbl.pack(pady=(5, 0), anchor="w")
            
            f_app1 = ttk.Frame(self.main_container)
            f_app1.pack(fill="x")
            ttk.Label(f_app1, text="Nombre:").grid(row=0, column=0, padx=5)
            setattr(self, f"app_name_{i}", ttk.Entry(f_app1))
            getattr(self, f"app_name_{i}").grid(row=0, column=1, sticky="ew", padx=2)
            
            ttk.Label(f_app1, text="Proceso .exe:").grid(row=0, column=2, padx=5)
            setattr(self, f"app_proc_{i}", ttk.Entry(f_app1))
            getattr(self, f"app_proc_{i}").grid(row=0, column=3, sticky="ew", padx=2)
            f_app1.columnconfigure((1, 3), weight=1)

            f_app2 = ttk.Frame(self.main_container)
            f_app2.pack(fill="x", pady=(2, 10))
            ttk.Label(f_app2, text="Ruta Executable:").grid(row=0, column=0, padx=5)
            setattr(self, f"app_path_{i}", ttk.Entry(f_app2))
            getattr(self, f"app_path_{i}").grid(row=0, column=1, sticky="ew", padx=2)
            
            btn_browse = ttk.Button(f_app2, text="...", width=3, command=lambda idx=i: self.browse_path(idx))
            btn_browse.grid(row=0, column=2, padx=2)
            f_app2.columnconfigure(1, weight=1)

        # Sección 4: Acciones
        self.create_section_header(self.main_container, "4. Acciones Finales")
        
        btn_frame = ttk.Frame(self.main_container)
        btn_frame.pack(fill="x", pady=10)
        
        self.btn_save = tk.Button(btn_frame, text="✅ GUARDAR Y CONFIGURAR", bg=COLORS["success"], fg="#000", font=("Segoe UI", 10, "bold"), command=self.save_settings, padding=10)
        self.btn_save.pack(side="left", fill="x", expand=True, padx=5)
        
        self.btn_startup = tk.Button(btn_frame, text="🚀 AÑADIR AL INICIO", bg=COLORS["accent"], fg="#000", font=("Segoe UI", 10, "bold"), command=self.add_to_startup, padding=10)
        self.btn_startup.pack(side="left", fill="x", expand=True, padx=5)

    def browse_path(self, idx):
        path = filedialog.askopenfilename(title=f"Seleccionar ejecutable para App {idx}")
        if path:
            getattr(self, f"app_path_{idx}").delete(0, tk.END)
            getattr(self, f"app_path_{idx}").insert(0, path)

    def load_data(self):
        # Cargar .env
        env_path = ".env"
        if os.path.exists(env_path):
            with open(env_path, "r", encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines:
                    if "=" in line:
                        k, v = line.strip().split("=", 1)
                        if k == "TELEGRAM_TOKEN": self.entry_token.insert(0, v)
                        elif k == "ADMIN_ID": self.entry_admin_id.insert(0, v)
                        elif k == "DISCORD_PATH": self.app_path_1.insert(0, v)
                        elif k == "STEAM_PATH": self.app_path_2.insert(0, v)
                        elif k == "STATS_CC_PATH": self.app_path_3.insert(0, v)

        # Cargar config.json
        config_path = "config.json"
        if os.path.exists(config_path):
            with open(config_path, "r", encoding='utf-8') as f:
                config = json.load(f)
                
                games = config.get("games", [])
                for i, game in enumerate(games[:2], 1):
                    getattr(self, f"game_name_{i}").insert(0, game.get("name", ""))
                    getattr(self, f"game_sid_{i}").insert(0, game.get("steam_id", ""))
                    getattr(self, f"game_proc_{i}").insert(0, game.get("process", ""))
                
                apps = config.get("apps", [])
                for i, app in enumerate(apps[:3], 1):
                    getattr(self, f"app_name_{i}").insert(0, app.get("name", ""))
                    getattr(self, f"app_proc_{i}").insert(0, app.get("process", ""))

    def save_settings(self):
        try:
            # 1. Guardar .env
            env_content = [
                f"TELEGRAM_TOKEN={self.entry_token.get()}",
                f"ADMIN_ID={self.entry_admin_id.get()}",
                f"DISCORD_PATH={self.app_path_1.get()}",
                f"STEAM_PATH={self.app_path_2.get()}",
                f"STATS_CC_PATH={self.app_path_3.get()}"
            ]
            with open(".env", "w", encoding='utf-8') as f:
                f.write("\n".join(env_content))

            # 2. Guardar config.json
            config = {
                "games": [],
                "apps": []
            }
            
            for i in range(1, 3):
                config["games"].append({
                    "id": str(i),
                    "name": getattr(self, f"game_name_{i}").get(),
                    "steam_id": getattr(self, f"game_sid_{i}").get(),
                    "process": getattr(self, f"game_proc_{i}").get()
                })
            
            env_keys = ["DISCORD_PATH", "STEAM_PATH", "STATS_CC_PATH"]
            for i in range(1, 4):
                config["apps"].append({
                    "id": str(i),
                    "name": getattr(self, f"app_name_{i}").get(),
                    "env_key": env_keys[i-1],
                    "process": getattr(self, f"app_proc_{i}").get()
                })
            
            with open("config.json", "w", encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)

            messagebox.showinfo("Éxito", "Configuración guardada correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la configuración: {e}")

    def add_to_startup(self):
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            bat_path = os.path.join(script_dir, "Bot_xrd.bat")
            startup_path = os.path.join(os.environ['APPDATA'], r'Microsoft\Windows\Start Menu\Programs\Startup')
            shortcut_path = os.path.join(startup_path, "Bot_xrd.lnk")
            
            # PowerShell command to create shortcut
            ps_cmd = f'$s=(New-Object -COM WScript.Shell).CreateShortcut("{shortcut_path}");$s.TargetPath="{bat_path}";$s.WorkingDirectory="{script_dir}";$s.IconLocation="{os.path.join(script_dir, "bot_xrd.ico")}";$s.Save()'
            subprocess.run(["powershell", "-Command", ps_cmd], check=True)
            
            messagebox.showinfo("Éxito", "El Bot se ha añadido al inicio de Windows correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo añadir al inicio: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SetupApp(root)
    root.mainloop()
