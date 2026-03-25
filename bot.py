import os
import time
import subprocess
import psutil
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# Cargar variables de entorno desde .env
load_dotenv()

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
    keyboard = [
        [InlineKeyboardButton("R6 Siege 🔓", callback_data='abrir_juego_1'), InlineKeyboardButton("R6 Siege ❌", callback_data='cerrar_juego_1')],
        [InlineKeyboardButton("ARC Raiders 🔓", callback_data='abrir_juego_2'), InlineKeyboardButton("ARC Raiders ❌", callback_data='cerrar_juego_2')],
        [InlineKeyboardButton("🔙 Volver", callback_data='menu_principal')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_apps_menu():
    keyboard = [
        [InlineKeyboardButton("Discord 🔓", callback_data='abrir_app_1'), InlineKeyboardButton("Discord ❌", callback_data='cerrar_app_1')],
        [InlineKeyboardButton("Steam 🔓", callback_data='abrir_app_2'), InlineKeyboardButton("Steam ❌", callback_data='cerrar_app_2')],
        [InlineKeyboardButton("stats.cc 🔓", callback_data='abrir_app_3'), InlineKeyboardButton("stats.cc ❌", callback_data='cerrar_app_3')],
        [InlineKeyboardButton("🔙 Volver", callback_data='menu_principal')]
    ]
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

# Esta función lee los mensajes de texto (para atrapar nombres de procesos)
async def recibir_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    texto = update.message.text
    
    # 1. Comprobar autorización por ID
    if user_id != MI_ID_TELEGRAM:
        return # Ignoramos por completo los mensajes de extraños

    # 2. Si está autorizado, comprobar si estamos esperando el nombre de un proceso para cerrar
    if context.user_data.get('esperando_proceso'):
        proceso_a_cerrar = texto.strip()
        # Limpiamos el estado para no seguir esperando
        context.user_data['esperando_proceso'] = False
        
        # Le añadimos .exe de forma segura si el usuario solo puso el nombre
        if not proceso_a_cerrar.endswith(".exe"):
            proceso_a_cerrar += ".exe"
            
        await update.message.reply_text(f"⏳ Intentando cerrar: {proceso_a_cerrar}...")
        
        # Ejecutamos taskkill en Windows
        comando = f'taskkill /IM "{proceso_a_cerrar}" /F'
        resultado = os.system(comando)
        
        if resultado == 0:
            await update.message.reply_text(f"✅ ¡El proceso {proceso_a_cerrar} se cerró correctamente!")
        else:
            await update.message.reply_text(f"❌ No se pudo cerrar {proceso_a_cerrar}. Puede que no exista o requiera permisos de administrador.")
            
        # Volvemos a mostrar el menú general de sistema
        await update.message.reply_text("🔧 **Submenú Sistema**\nOpciones de energía y control:", parse_mode='Markdown', reply_markup=get_system_menu())

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # 🚨 SISTEMA DE SEGURIDAD PARA LOS BOTONES 🚨
    if update.effective_user.id != MI_ID_TELEGRAM:
        return # Ignoramos la pulsación del botón si no es tu ID
        
    query = update.callback_query
    await query.answer()
    opcion = query.data

    # --- NAVEGACIÓN ---
    if opcion == 'menu_principal':
        await query.edit_message_text(text="🖥️ **MENÚ PRINCIPAL**\nElige una categoría:", parse_mode='Markdown', reply_markup=get_main_menu())
    
    elif opcion == 'menu_juegos':
        await query.edit_message_text(text="🎮 **Submenú Juegos**\n¿A qué jugamos hoy?", parse_mode='Markdown', reply_markup=get_games_menu())
        
    elif opcion == 'menu_aplicaciones':
        await query.edit_message_text(text="💻 **Submenú Aplicaciones**\nControl de programas:", parse_mode='Markdown', reply_markup=get_apps_menu())
        
    elif opcion == 'menu_sistema':
        await query.edit_message_text(text="🔧 **Submenú Sistema**\nOpciones de energía:", parse_mode='Markdown', reply_markup=get_system_menu())
        
    elif opcion == 'menu_multimedia':
        await query.edit_message_text(text="🎵 **Submenú Multimedia**\nControl de entretenimiento:", parse_mode='Markdown', reply_markup=get_multimedia_menu())

    # --- ACCIÓN: LIMPIAR CHAT ---
    elif opcion == 'limpiar_chat':
        await query.edit_message_text(text="🗑️ Limpiando mensajes antiguos...")
        chat_id = update.effective_chat.id
        message_id = query.message.message_id
        borrados = 0
        # Intentamos borrar los últimos 100 mensajes anteriores al actual
        for i in range(1, 100):
            try:
                await context.bot.delete_message(chat_id=chat_id, message_id=message_id - i)
                borrados += 1
            except Exception:
                pass # Si no puede borrar un mensaje, lo saltamos
        # Mostramos el menú de nuevo con el resultado
        await query.edit_message_text(text=f"✅ Chat limpio. {borrados} mensajes borrados.", reply_markup=get_main_menu())

    # --- ACCIONES: JUEGOS (via Steam) ---
    elif opcion == 'abrir_juego_1':
        await query.edit_message_text(text="🎮 Iniciando Rainbow Six Siege via Steam...", reply_markup=get_games_menu())
        os.system("start steam://rungameid/359550")
        
    elif opcion == 'cerrar_juego_1':
        os.system("taskkill /IM RainbowSix.exe /F")
        os.system("taskkill /IM RainbowSix_Vulkan.exe /F")
        await query.edit_message_text(text="❌ Rainbow Six Siege cerrado.", reply_markup=get_games_menu())

    elif opcion == 'abrir_juego_2':
        await query.edit_message_text(text="🎮 Iniciando ARC Raiders via Steam...", reply_markup=get_games_menu())
        os.system("start steam://rungameid/1808500")
        
    elif opcion == 'cerrar_juego_2':
        os.system("taskkill /IM ARC-Win64-Shipping.exe /F")
        await query.edit_message_text(text="❌ ARC Raiders cerrado.", reply_markup=get_games_menu())

    # --- ACCIONES: APLICACIONES ---
    elif opcion == 'abrir_app_1':
        await query.edit_message_text(text="🔓 Abriendo Discord...", reply_markup=get_apps_menu())
        # Ruta personalizable via .env o valor por defecto
        ruta_discord = os.getenv('DISCORD_PATH', r"C:\Path\To\Discord\Update.exe")
        argumentos = ["--processStart", "Discord.exe"]
        if os.path.exists(ruta_discord):
            subprocess.Popen([ruta_discord] + argumentos)
        else:
            await query.edit_message_text(text="❌ Error: No se encontró la ruta de Discord. Configúrala en el archivo .env", reply_markup=get_apps_menu())
        
    elif opcion == 'cerrar_app_1':
        os.system("taskkill /IM Discord.exe /F")
        await query.edit_message_text(text="❌ Discord cerrado.", reply_markup=get_apps_menu())

    elif opcion == 'abrir_app_2':
        await query.edit_message_text(text="🔓 Abriendo Steam...", reply_markup=get_apps_menu())
        ruta_steam = os.getenv('STEAM_PATH', r"C:\Program Files (x86)\Steam\Steam.exe")
        if os.path.exists(ruta_steam):
            subprocess.Popen([ruta_steam])
        else:
            await query.edit_message_text(text="❌ Error: No se encontró la ruta de Steam. Configúrala en el archivo .env", reply_markup=get_apps_menu())
        
    elif opcion == 'cerrar_app_2':
        os.system("taskkill /IM steam.exe /F")
        await query.edit_message_text(text="❌ Steam cerrado.", reply_markup=get_apps_menu())

    elif opcion == 'abrir_app_3':
        await query.edit_message_text(text="🔓 Abriendo stats.cc...", reply_markup=get_apps_menu())
        ruta_stats = os.getenv('STATS_CC_PATH', r"C:\Path\To\stats.cc.exe")
        if os.path.exists(ruta_stats):
            subprocess.Popen([ruta_stats])
        else:
            await query.edit_message_text(text="❌ Error: No se encontró la ruta de stats.cc. Configúrala en el archivo .env", reply_markup=get_apps_menu())
        
    elif opcion == 'cerrar_app_3':
        os.system('taskkill /IM "stats.cc.exe" /F')
        await query.edit_message_text(text="❌ stats.cc cerrado.", reply_markup=get_apps_menu())

    # --- ACCIONES: SISTEMA ---
    elif opcion == 'sistema_procesos':
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

    elif opcion == 'sistema_cerrar_proceso':
        # Activamos el estado "esperando mensaje del usuario"
        context.user_data['esperando_proceso'] = True
        await query.edit_message_text(text="❌ **CERRAR PROCESO**\n\nEscribe el nombre del proceso que quieres cerrar y envíame el mensaje.\n\nEjemplos: `Spotify.exe`, `chrome`, `Discord`")
        
    elif opcion == 'sistema_apagar':
        await query.edit_message_text(text="⏻ ¡Apagando el PC en 5 segundos!", reply_markup=get_main_menu())
        os.system("shutdown /s /t 5")
    
    elif opcion == 'sistema_reiniciar':
        await query.edit_message_text(text="🔄 ¡Reiniciando el PC en 5 segundos!", reply_markup=get_main_menu())
        os.system("shutdown /r /t 5")

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
