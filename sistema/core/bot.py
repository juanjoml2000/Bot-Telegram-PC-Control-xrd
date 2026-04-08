import os
import time
import subprocess
import psutil
import json
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# Directorio raíz del proyecto
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Cargar variables de entorno desde .env en la raíz
load_dotenv(os.path.join(ROOT_DIR, '.env'))

# Cargar configuración desde config.json en la raíz
CONFIG_PATH = os.path.join(ROOT_DIR, 'config.json')
if os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        config = json.load(f)
else:
    # Configuración por defecto si no existe el archivo
    config = {"games": [], "apps": []}

TOKEN = os.getenv('TELEGRAM_TOKEN', 'TU_TOKEN_AQUI')
# ID de administrador autorizado
MI_ID_TELEGRAM = int(os.getenv('ADMIN_ID', '0'))

# --- FUNCIONES DE LOS MENÚS ---

def get_main_menu():
    keyboard = [
        [InlineKeyboardButton("🎮 Juegos", callback_data='menu_juegos')],
        [InlineKeyboardButton("💻 Aplicaciones", callback_data='menu_aplicaciones')],
        [InlineKeyboardButton("🔧 Sistema", callback_data='menu_sistema')],
        [InlineKeyboardButton("🎵 Multimedia", callback_data='menu_multimedia')],
        [InlineKeyboardButton("🗑️ Limpiar chat", callback_data='limpiar_chat')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_games_menu():
    keyboard = []
    for game in config.get('games', []):
        name = game['name']
        gid = game['id']
        keyboard.append([
            InlineKeyboardButton(f"{name} 🔓", callback_data=f'abrir_juego_{gid}'),
            InlineKeyboardButton(f"{name} ❌", callback_data=f'cerrar_juego_{gid}')
        ])
    keyboard.append([InlineKeyboardButton("🔙 Volver", callback_data='menu_principal')])
    return InlineKeyboardMarkup(keyboard)

def get_apps_menu():
    keyboard = []
    for app in config.get('apps', []):
        name = app['name']
        aid = app['id']
        keyboard.append([
            InlineKeyboardButton(f"{name} 🔓", callback_data=f'abrir_app_{aid}'),
            InlineKeyboardButton(f"{name} ❌", callback_data=f'cerrar_app_{aid}')
        ])
    keyboard.append([InlineKeyboardButton("🔙 Volver", callback_data='menu_principal')])
    return InlineKeyboardMarkup(keyboard)

def get_system_menu():
    keyboard = [
        [InlineKeyboardButton("🖥️ Procesos", callback_data='sistema_procesos'), InlineKeyboardButton("❌ Cerrar proceso", callback_data='sistema_cerrar_proceso')],
        [InlineKeyboardButton("🔄 Reiniciar", callback_data='sistema_reiniciar'), InlineKeyboardButton("⏻ Apagar", callback_data='sistema_apagar')],
        [InlineKeyboardButton("🔙 Volver", callback_data='menu_principal')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_multimedia_menu():
    keyboard = [
        [InlineKeyboardButton("YouTube 🔓", callback_data='abrir_youtube'), InlineKeyboardButton("YouTube ❌", callback_data='cerrar_youtube')],
        [InlineKeyboardButton("Spotify 🔓", callback_data='abrir_spotify'), InlineKeyboardButton("Spotify ❌", callback_data='cerrar_spotify')],
        [InlineKeyboardButton("🔙 Volver", callback_data='menu_principal')]
    ]
    return InlineKeyboardMarkup(keyboard)

# --- MANEJADORES ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if user_id != MI_ID_TELEGRAM:
        print(f"⚠️ Intento de acceso bloqueado del usuario ID: {user_id}")
        await update.message.reply_text("⛔ Acceso denegado. Este es un bot privado para control de PC.")
        return
        
    await update.message.reply_text('🖥️ **MENÚ PRINCIPAL**\nElige una categoría:', parse_mode='Markdown', reply_markup=get_main_menu())

async def recibir_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    texto = update.message.text
    
    if user_id != MI_ID_TELEGRAM:
        return

    if context.user_data.get('esperando_proceso'):
        proceso_a_cerrar = texto.strip()
        context.user_data['esperando_proceso'] = False
        
        if not proceso_a_cerrar.endswith(".exe"):
            proceso_a_cerrar += ".exe"
            
        await update.message.reply_text(f"⏳ Intentando cerrar: {proceso_a_cerrar}...")
        
        comando = f'taskkill /IM "{proceso_a_cerrar}" /F'
        resultado = os.system(comando)
        
        if resultado == 0:
            await update.message.reply_text(f"✅ ¡El proceso {proceso_a_cerrar} se cerró correctamente!")
        else:
            await update.message.reply_text(f"❌ No se pudo cerrar {proceso_a_cerrar}. Puede que no exista o requiera permisos de administrador.")
            
        await update.message.reply_text("🔧 **Submenú Sistema**\nOpciones de energía y control:", parse_mode='Markdown', reply_markup=get_system_menu())

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id != MI_ID_TELEGRAM:
        return
        
    query = update.callback_query
    await query.answer()
    opcion = query.data

    # --- NAVEGACIÓN ---
    if opcion == 'menu_principal':
        await query.edit_message_text(text="🖥️ **MENÚ PRINCIPAL**\nElige una categoría:", parse_mode='Markdown', reply_markup=get_main_menu())
        return
    
    elif opcion == 'menu_juegos':
        await query.edit_message_text(text="🎮 **Submenú Juegos**\n¿A qué jugamos hoy?", parse_mode='Markdown', reply_markup=get_games_menu())
        return
        
    elif opcion == 'menu_aplicaciones':
        await query.edit_message_text(text="💻 **Submenú Aplicaciones**\nControl de programas:", parse_mode='Markdown', reply_markup=get_apps_menu())
        return
        
    elif opcion == 'menu_sistema':
        await query.edit_message_text(text="🔧 **Submenú Sistema**\nOpciones de energía:", parse_mode='Markdown', reply_markup=get_system_menu())
        return
        
    elif opcion == 'menu_multimedia':
        await query.edit_message_text(text="🎵 **Submenú Multimedia**\nControl de entretenimiento:", parse_mode='Markdown', reply_markup=get_multimedia_menu())
        return

    # --- ACCIÓN: LIMPIAR CHAT ---
    elif opcion == 'limpiar_chat':
        await query.edit_message_text(text="🗑️ Limpiando mensajes antiguos...")
        chat_id = update.effective_chat.id
        message_id = query.message.message_id
        borrados = 0
        for i in range(1, 100):
            try:
                await context.bot.delete_message(chat_id=chat_id, message_id=message_id - i)
                borrados += 1
            except Exception:
                pass
        await query.edit_message_text(text=f"✅ Chat limpio. {borrados} mensajes borrados.", reply_markup=get_main_menu())
        return

    # --- ACCIONES DINÁMICAS: JUEGOS ---
    for game in config.get('games', []):
        gid = str(game['id'])
        if opcion == f'abrir_juego_{gid}':
            await query.edit_message_text(text=f"🎮 Iniciando {game['name']} via Steam...", reply_markup=get_games_menu())
            os.system(f"start steam://rungameid/{game['steam_id']}")
            return
        elif opcion == f'cerrar_juego_{gid}':
            os.system(f'taskkill /IM "{game["process"]}" /F')
            if "RainbowSix" in game["process"]:
                os.system("taskkill /IM RainbowSix_Vulkan.exe /F")
            await query.edit_message_text(text=f"❌ {game['name']} cerrado.", reply_markup=get_games_menu())
            return

    # --- ACCIONES DINÁMICAS: APLICACIONES ---
    for app in config.get('apps', []):
        aid = str(app['id'])
        if opcion == f'abrir_app_{aid}':
            await query.edit_message_text(text=f"🔓 Abriendo {app['name']}...", reply_markup=get_apps_menu())
            ruta = os.getenv(app['env_key'])
            argumentos = []
            if "Discord" in app['name']:
                argumentos = ["--processStart", "Discord.exe"]
            if ruta and os.path.exists(ruta):
                subprocess.Popen([ruta] + argumentos)
            else:
                await query.edit_message_text(text=f"❌ Error: Ruta no encontrada para {app['name']}. Revisa el .env ({app['env_key']})", reply_markup=get_apps_menu())
            return
        elif opcion == f'cerrar_app_{aid}':
            os.system(f'taskkill /IM "{app["process"]}" /F')
            await query.edit_message_text(text=f"❌ {app['name']} cerrado.", reply_markup=get_apps_menu())
            return

    # --- ACCIONES: SISTEMA ---
    if opcion == 'sistema_procesos':
        await query.edit_message_text(text="⏳ Recopilando lista de procesos...")
        try:
            procesos = []
            for proc in psutil.process_iter(['name', 'memory_info']):
                try:
                    pinfo = proc.info
                    memoria_mb = pinfo['memory_info'].rss / (1024 * 1024)
                    procesos.append({'name': pinfo['name'], 'mem': memoria_mb})
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
            procesos = sorted(procesos, key=lambda p: p['mem'], reverse=True)
            texto_procesos = "🖥️ **Top 15 Procesos (RAM)**\n\n"
            for p in procesos[:15]:
                texto_procesos += f"• `{p['name']}` - {p['mem']:.1f} MB\n"
            texto_procesos += "\n_Usa 'Cerrar proceso' para matar alguno._"
            await query.edit_message_text(text=texto_procesos, parse_mode='Markdown', reply_markup=get_system_menu())
        except Exception as e:
            await query.edit_message_text(text=f"⚠️ Error al obtener procesos: {e}", reply_markup=get_system_menu())
        return

    elif opcion == 'sistema_cerrar_proceso':
        context.user_data['esperando_proceso'] = True
        await query.edit_message_text(text="❌ **CERRAR PROCESO**\n\nEscribe el nombre del proceso que quieres cerrar y envíame el mensaje.\n\nEjemplos: `Spotify.exe`, `chrome`, `Discord`")
        return
        
    elif opcion == 'sistema_apagar':
        await query.edit_message_text(text="⏻ ¡Apagando el PC en 5 segundos!", reply_markup=get_main_menu())
        os.system("shutdown /s /t 5")
        return
    
    elif opcion == 'sistema_reiniciar':
        await query.edit_message_text(text="🔄 ¡Reiniciando el PC en 5 segundos!", reply_markup=get_main_menu())
        os.system("shutdown /r /t 5")
        return

    # --- ACCIONES: MULTIMEDIA ---
    elif opcion == 'abrir_youtube':
        await query.edit_message_text(text="🔓 Abriendo YouTube...", reply_markup=get_multimedia_menu())
        os.system("start https://www.youtube.com")
        
    elif opcion == 'cerrar_youtube':
        os.system("taskkill /IM chrome.exe /F")
        os.system("taskkill /IM msedge.exe /F")
        await query.edit_message_text(text="❌ Navegador cerrado.", reply_markup=get_multimedia_menu())

    elif opcion == 'abrir_spotify':
        await query.edit_message_text(text="🔓 Abriendo Spotify...", reply_markup=get_multimedia_menu())
        os.system("start spotify:")
        
    elif opcion == 'cerrar_spotify':
        os.system("taskkill /IM Spotify.exe /F")
        await query.edit_message_text(text="❌ Spotify cerrado.", reply_markup=get_multimedia_menu())

application = None

def main() -> None:
    global application
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_mensaje))
    application.add_handler(CallbackQueryHandler(button))
    
    print("Bot iniciado. Esperando órdenes...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
