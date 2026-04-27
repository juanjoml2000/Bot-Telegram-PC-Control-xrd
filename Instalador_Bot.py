import os
import sys
import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import stat

# Asegurar que estamos en el directorio del script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

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
        self.root.geometry("700x900")
        self.root.configure(bg=COLORS["bg"])

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TFrame", background=COLORS["bg"])
        self.style.configure("TLabel", background=COLORS["bg"], foreground=COLORS["fg"], font=("Segoe UI", 10))
        self.style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"), foreground=COLORS["accent"])
        self.style.configure("TEntry", fieldbackground=COLORS["secondary"], foreground=COLORS["fg"])
        self.style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"))

        self.canvas = tk.Canvas(root, bg=COLORS["bg"], highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        
        self.main_container = ttk.Frame(self.canvas, padding="20")
        
        self.main_container.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.frame_id = self.canvas.create_window((0, 0), window=self.main_container, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(self.frame_id, width=e.width)
        )
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        root.bind_all("<MouseWheel>", _on_mousewheel)

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
            
            btn_browse_game = ttk.Button(f_game, text="...", width=3, command=lambda idx=i: self.browse_path_game(idx))
            btn_browse_game.grid(row=0, column=6, padx=2)
            
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

        # Sección 4: Opciones
        self.create_section_header(self.main_container, "4. Opciones")
        
        self.reinstall_deps = tk.BooleanVar(value=False)
        chk_deps = tk.Checkbutton(
            self.main_container, text="🔄 Reinstalar dependencias (pip install)",
            variable=self.reinstall_deps, bg=COLORS["bg"], fg=COLORS["fg"],
            selectcolor=COLORS["secondary"], activebackground=COLORS["bg"],
            activeforeground=COLORS["fg"], font=("Segoe UI", 10)
        )
        chk_deps.pack(anchor="w", pady=(5, 10))

        # Sección 5: Acciones
        self.create_section_header(self.main_container, "5. Acciones Finales")
        
        btn_frame1 = ttk.Frame(self.main_container)
        btn_frame1.pack(fill="x", pady=(10, 5))
        
        self.btn_save = tk.Button(btn_frame1, text="✅ GUARDAR CONFIG", bg=COLORS["success"], fg="#000", font=("Segoe UI", 10, "bold"), command=self.save_settings, padx=10, pady=10)
        self.btn_save.pack(side="left", fill="x", expand=True, padx=5)
        
        self.btn_desktop = tk.Button(btn_frame1, text="📌 CREAR EN ESCRITORIO", bg="#cba6f7", fg="#000", font=("Segoe UI", 10, "bold"), command=self.add_to_desktop, padx=10, pady=10)
        self.btn_desktop.pack(side="left", fill="x", expand=True, padx=5)

        btn_frame2 = ttk.Frame(self.main_container)
        btn_frame2.pack(fill="x", pady=(5, 10))

        self.btn_startup = tk.Button(btn_frame2, text="🚀 AÑADIR A INICIO", bg=COLORS["accent"], fg="#000", font=("Segoe UI", 10, "bold"), command=self.add_to_startup, padx=10, pady=10)
        self.btn_startup.pack(side="left", fill="x", expand=True, padx=5)

        self.btn_remove_startup = tk.Button(btn_frame2, text="❌ QUITAR DE INICIO", bg=COLORS["error"], fg="#000", font=("Segoe UI", 10, "bold"), command=self.remove_from_startup, padx=10, pady=10)
        self.btn_remove_startup.pack(side="left", fill="x", expand=True, padx=5)

    def browse_path(self, idx):
        path = filedialog.askopenfilename(title=f"Seleccionar ejecutable para App {idx}", filetypes=[("Ejecutables", "*.exe"), ("Todos los archivos", "*.*")])
        if path:
            # Rellenar ruta
            getattr(self, f"app_path_{idx}").delete(0, tk.END)
            getattr(self, f"app_path_{idx}").insert(0, path)
            
            # Autocompletar nombre de proceso
            exe_name = os.path.basename(path)
            getattr(self, f"app_proc_{idx}").delete(0, tk.END)
            getattr(self, f"app_proc_{idx}").insert(0, exe_name)
            
            # Si el nombre de la app está vacío, sugerir el nombre del archivo (sin .exe)
            if not getattr(self, f"app_name_{idx}").get().strip():
                name_suggest = os.path.splitext(exe_name)[0].capitalize()
                getattr(self, f"app_name_{idx}").insert(0, name_suggest)

    def browse_path_game(self, idx):
        path = filedialog.askopenfilename(title=f"Seleccionar ejecutable para Juego {idx}", filetypes=[("Ejecutables", "*.exe"), ("Todos los archivos", "*.*")])
        if path:
            exe_name = os.path.basename(path)
            # Rellenar proceso
            getattr(self, f"game_proc_{idx}").delete(0, tk.END)
            getattr(self, f"game_proc_{idx}").insert(0, exe_name)
            
            # Si el nombre del juego está vacío, sugerir el nombre del archivo
            if not getattr(self, f"game_name_{idx}").get().strip():
                name_suggest = os.path.splitext(exe_name)[0].capitalize()
                getattr(self, f"game_name_{idx}").insert(0, name_suggest)

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
                        elif k == "APP1_PATH": self.app_path_1.insert(0, v)
                        elif k == "APP2_PATH": self.app_path_2.insert(0, v)
                        elif k == "APP3_PATH": self.app_path_3.insert(0, v)

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
            # 1. Preparar y Guardar .env
            env_path = ".env"
            # Intentar quitar atributo de solo lectura si existe
            if os.path.exists(env_path):
                try:
                    os.chmod(env_path, stat.S_IWRITE)
                except:
                    pass

            env_content = [
                f"TELEGRAM_TOKEN={self.entry_token.get().strip()}",
                f"ADMIN_ID={self.entry_admin_id.get().strip()}",
                f"APP1_PATH={self.app_path_1.get().strip()}",
                f"APP2_PATH={self.app_path_2.get().strip()}",
                f"APP3_PATH={self.app_path_3.get().strip()}"
            ]
            
            try:
                with open(env_path, "w", encoding='utf-8') as f:
                    f.write("\n".join(env_content))
            except PermissionError:
                messagebox.showerror("Error de Permisos", "No se pudo escribir en el archivo '.env'.\n\nPOSIBLE SOLUCIÓN:\n1. Cierra el Bot (bot_tray.pyw) si se está ejecutando en segundo plano.\n2. Asegúrate de tener permisos de administrador.\n3. Revisa que el archivo no esté abierto en otro programa.")
                return

            # 2. Guardar config.json
            config = {
                "games": [],
                "apps": []
            }
            
            # Filtrar solo juegos que tengan nombre
            valid_game_count = 1
            for i in range(1, 3):
                name = getattr(self, f"game_name_{i}").get().strip()
                if name:
                    config["games"].append({
                        "id": str(valid_game_count),
                        "name": name,
                        "steam_id": getattr(self, f"game_sid_{i}").get().strip(),
                        "process": getattr(self, f"game_proc_{i}").get().strip()
                    })
                    valid_game_count += 1
            
            # Filtrar solo apps que tengan nombre
            env_keys = ["APP1_PATH", "APP2_PATH", "APP3_PATH"]
            valid_app_count = 1
            for i in range(1, 4):
                name = getattr(self, f"app_name_{i}").get().strip()
                if name:
                    config["apps"].append({
                        "id": str(valid_app_count),
                        "name": name,
                        "env_key": env_keys[i-1],
                        "process": getattr(self, f"app_proc_{i}").get().strip()
                    })
                    valid_app_count += 1
            
            with open("config.json", "w", encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)

            # 3. Instalar dependencias solo si el checkbox está marcado
            if self.reinstall_deps.get():
                try:
                    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "sistema/requirements.txt"], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
                    messagebox.showinfo("Éxito", "Configuración guardada y dependencias reinstaladas correctamente.")
                except Exception as pip_e:
                    messagebox.showwarning("Aviso", f"Configuración guardada, pero hubo un problema al instalar las dependencias:\n{pip_e}\n\nPor favor, ejecuta 'pip install -r sistema/requirements.txt' manualmente.")
            else:
                messagebox.showinfo("Éxito", "✅ Configuración guardada correctamente.\n\n(Las dependencias no se reinstalaron. Marca la casilla si necesitas reinstalarlas.)")

        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado al guardar: {e}")

    def _get_shortcut_params(self):
        """Devuelve los parámetros comunes para crear accesos directos."""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        core_dir = os.path.join(script_dir, "sistema", "core")
        assets_dir = os.path.join(script_dir, "sistema", "assets")
        bot_tray_path = os.path.join(core_dir, "bot_tray.pyw")
        
        pythonw_path = sys.executable.replace("python.exe", "pythonw.exe")
        if not os.path.exists(pythonw_path):
            pythonw_path = "pythonw"
        
        icon_path = os.path.join(assets_dir, "bot_xrd.ico")
        return pythonw_path, bot_tray_path, core_dir, icon_path

    def _create_shortcut(self, shortcut_path):
        """Crea un acceso directo .lnk en la ruta indicada."""
        pythonw_path, bot_tray_path, core_dir, icon_path = self._get_shortcut_params()
        ps_cmd = f'$s=(New-Object -COM WScript.Shell).CreateShortcut("{shortcut_path}");$s.TargetPath="{pythonw_path}";$s.Arguments="`"{bot_tray_path}`"";$s.WorkingDirectory="{core_dir}";$s.IconLocation="{icon_path}";$s.Save()'
        subprocess.run(["powershell", "-Command", ps_cmd], check=True, creationflags=subprocess.CREATE_NO_WINDOW)

    def add_to_startup(self):
        try:
            startup_path = os.path.join(os.environ['APPDATA'], r'Microsoft\Windows\Start Menu\Programs\Startup')
            shortcut_path = os.path.join(startup_path, "Bot_xrd.lnk")
            self._create_shortcut(shortcut_path)
            messagebox.showinfo("Éxito", "✅ El Bot se ha añadido al inicio de Windows correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo añadir al inicio: {e}")

    def remove_from_startup(self):
        try:
            startup_path = os.path.join(os.environ['APPDATA'], r'Microsoft\Windows\Start Menu\Programs\Startup')
            shortcut_path = os.path.join(startup_path, "Bot_xrd.lnk")
            if os.path.exists(shortcut_path):
                os.remove(shortcut_path)
                messagebox.showinfo("Éxito", "✅ Se ha quitado el bot del inicio de Windows correctamente.")
            else:
                messagebox.showinfo("Información", "El bot no estaba configurado para iniciar con Windows.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo quitar del inicio: {e}")

    def add_to_desktop(self):
        try:
            desktop_path = os.path.join(os.environ['USERPROFILE'], 'Desktop')
            shortcut_path = os.path.join(desktop_path, "Bot XRD.lnk")
            self._create_shortcut(shortcut_path)
            messagebox.showinfo("Éxito", "✅ Acceso directo creado en el Escritorio.\n\nHaz doble clic en 'Bot XRD' para lanzar el bot.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear el acceso directo: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SetupApp(root)
    root.mainloop()
