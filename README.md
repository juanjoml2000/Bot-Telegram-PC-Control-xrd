# 🤖 Bot-Telegram-PC-Control-xrd

Un potente bot de Telegram diseñado para el control remoto total de tu PC con Windows. Administra aplicaciones, juegos, procesos del sistema y contenido multimedia directamente desde tu móvil.

---

## ✨ Características principales

- 🎮 **Control de Juegos**: Inicia y cierra juegos de Steam (Rainbow Six Siege, ARC Raiders, etc.).
- 💻 **Gestión de Aplicaciones**: Abre y cierra Discord, Steam y stats.cc.
- 🔧 **Herramientas de Sistema**:
  - Monitor de procesos (Top 15 por uso de RAM).
  - Cierre forzado de procesos por nombre.
  - Reinicio y Apagado remoto del PC.
- 🎵 **Multimedia**: Control de YouTube (vía navegador) y Spotify.
- 🗑️ **Limpieza Automática**: Función para limpiar el historial del chat del bot.
- 🛡️ **Seguridad**: Sistema de bloqueo por ID de Telegram para que solo tú puedas controlarlo.
- 📥 **Bandeja de Sistema**: Icono en la barra de tareas para saber si el bot está activo.

---

## 🚀 Requisitos previos

1.  **Python 3.10+** instalado en el PC.
2.  **Git** (opcional, para clonar el repo).
3.  Una cuenta de **Telegram**.

---

## 🛠️ Configuración inicial

### 1. Preparación en Telegram (Paso a Paso)

Antes de ejecutar el bot, necesitas obtener tu Token y tu ID personal:

1.  **Obtener el Token del Bot**:
    - Busca a [@BotFather](https://t.me/botfather) en Telegram.
    - Escribe `/newbot` y sigue las instrucciones para darle un nombre y un nombre de usuario.
    - BotFather te dará un **API Token** (ej: `123456789:ABCDefgh...`). Guárdalo.
2.  **Obtener tu ID de Usuario**:
    - Busca a [@userinfobot](https://t.me/userinfobot) o [@RawDataBot](https://t.me/rawdatabot).
    - Envíale un mensaje y te responderá con tu `id` numérico (ej: `7747532155`). Este es el ID que el bot usará para obedecerte solo a ti.

### 2. Instalación local

1.  Clona este repositorio o descarga los archivos.
2.  Instala las dependencias necesarias:
    ```bash
    pip install -r requirements.txt
    ```
3.  Crea un archivo llamado `.env` en la carpeta raíz (puedes copiar el contenido de `.env.example`) y rellena tus datos:
    ```env
    TELEGRAM_TOKEN=TU_TOKEN_AQUI
    ADMIN_ID=TU_ID_DE_USUARIO
    DISCORD_PATH=C:\Ruta\A\Discord\Update.exe
    STEAM_PATH=C:\Program Files (x86)\Steam\Steam.exe
    STATS_CC_PATH=C:\Ruta\A\stats.cc.exe
    ```

---

## ⚙️ Uso

Para iniciar el bot tienes dos opciones:

- **Modo normal**: Ejecuta `python bot.py`. Se abrirá una ventana de consola.
- **Modo silencioso (con icono en tray)**: Ejecuta `pythonw bot_tray.pyw`. El bot se quedará en segundo plano y verás un icono en la bandeja del sistema (junto al reloj).

Una vez activo, ve a tu bot en Telegram y escribe `/start` para desplegar el menú interactivo.

---

## 🛠️ Tecnologías usadas

- [Python](https://www.python.org/)
- [python-telegram-bot](https://python-telegram-bot.org/) - Framework para la interacción con Telegram.
- [psutil](https://github.com/giampaolo/psutil) - Gestión de procesos y sistema.
- [pystray](https://github.com/moshekaplan/pystray) - Implementación del icono en la bandeja del sistema.
- [python-dotenv](https://github.com/theskumar/python-dotenv) - Gestión segura de variables de entorno.

---

## 📄 Licencia

Este proyecto es de uso personal y educativo. Siéntete libre de modificarlo para tus necesidades propias.

---

> [!TIP]
> **Seguridad**: Nunca compartas tu archivo `.env` ni tu API Token con nadie. Estos datos son privados y dan control total sobre tu PC.
