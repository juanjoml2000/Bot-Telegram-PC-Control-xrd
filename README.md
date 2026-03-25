# Bot-Telegram-PC-Control-xrd

Un potente bot de Telegram diseñado para el control remoto total de un PC con Windows. Administra aplicaciones, juegos, procesos del sistema y contenido multimedia directamente desde un dispositivo movil.

---

## Caracteristicas principales

- **Control de Juegos**: Inicia y cierra juegos de Steam (Rainbow Six Siege, ARC Raiders, etc.).
- **Gestion de Aplicaciones**: Abre y cierra Discord, Steam y stats.cc.
- **Herramientas de Sistema**:
  - Monitor de procesos (Top 15 por uso de RAM).
  - Cierre forzado de procesos por nombre.
  - Reinicio y Apagado remoto del PC.
- **Multimedia**: Control de YouTube (via navegador) y Spotify.
- **Limpieza Automatica**: Funcion para limpiar el historial del chat del bot.
- **Seguridad**: Sistema de bloqueo por ID de Telegram para acceso restringido al administrador.
- **Bandeja de Sistema**: Icono en la barra de tareas para monitorizar el estado del bot.

---

## Requisitos previos

1.  **Python 3.10+** instalado en el sistema.
2.  **Git** (opcional, para clonar el repositorio).
3.  Una cuenta de **Telegram**.

---

## Configuracion inicial

### 1. Preparacion en Telegram

Antes de ejecutar el bot, es necesario obtener un Token y el ID personal:

1.  **Obtener el Token del Bot**:
    - Contactar con [@BotFather](https://t.me/botfather) en Telegram.
    - Enviar el comando `/newbot` y seguir las instrucciones.
    - BotFather proporcionara un **API Token** (ejemplo: `123456789:ABCDefgh...`).
2.  **Obtener el ID de Usuario**:
    - Contactar con bots como [@userinfobot](https://t.me/userinfobot) o [@RawDataBot](https://t.me/rawdatabot).
    - Al enviar un mensaje, responderan con un `id` numérico (ejemplo: `123456789`). Este ID garantiza que solo el administrador pueda controlar el PC.

### 2. Instalacion local

1.  Descargar o clonar los archivos del repositorio.
2.  Instalar las dependencias necesarias:
    ```bash
    pip install -r requirements.txt
    ```
3.  Crear un archivo llamado `.env` en la carpeta raiz (basado en `.env.example`) y completar la informacion:
    ```env
    TELEGRAM_TOKEN=TU_TOKEN_AQUI
    ADMIN_ID=123456789
    DISCORD_PATH=C:\Ruta\A\Discord\Update.exe
    STEAM_PATH=C:\Program Files (x86)\Steam\Steam.exe
    STATS_CC_PATH=C:\Ruta\A\stats.cc.exe
    ```

---

## Uso

Existen dos opciones para iniciar el bot:

- **Modo estandar**: Ejecutar `python bot.py`. Se abrira una ventana de consola.
- **Modo segundo plano (con icono en tray)**: Ejecutar `pythonw bot_tray.pyw`. El bot se ejecutara silenciosamente con un icono en la bandeja del sistema.

Una vez activo, enviar el comando `/start` al bot en Telegram para desplegar el menu interactivo.

---

## Tecnologias utilizadas

- [Python](https://www.python.org/)
- [python-telegram-bot](https://python-telegram-bot.org/) - Interaccion con la API de Telegram.
- [psutil](https://github.com/giampaolo/psutil) - Gestion de procesos del sistema.
- [pystray](https://github.com/moshekaplan/pystray) - Icono en la bandeja del sistema.
- [python-dotenv](https://github.com/theskumar/python-dotenv) - Gestion segura de configuracion.

---

## Licencia

Este proyecto es de uso personal y educativo.

---

> [!TIP]
> **Seguridad**: Nunca comparta su archivo `.env` ni su API Token. Estos datos otorgan control total sobre el sistema.
