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
3.  **Cambiar la foto del Bot**:
    - En el mismo chat de [@BotFather](https://t.me/botfather), enviar el comando `/setuserpic`.
    - Seleccionar el bot de la lista.
    - Adjuntar y enviar la imagen que se desee establecer como perfil (puedes usar el archivo `icon_xrd.png` incluido en este repositorio).
4.  **Obtener el ID de Usuario**:
    - Contactar con bots como [@userinfobot](https://t.me/userinfobot) o [@RawDataBot](https://t.me/rawdatabot).
    - Al enviar un mensaje, responderan con un `id` numérico (ejemplo: `123456789`). Este ID garantiza que solo el administrador pueda controlar el PC.

### Estructura del Proyecto

```text
📁 bot-telegram
 ├── 🚀 1_Instalar_Python.bat (Instala Python si no lo tienes y abre el instalador)
 ├── 🗑️ 2_Desinstalar_Python.bat (Remueve Python del sistema de forma silenciosa)
 ├── ⚙️ Instalador_Bot.py    (Instalador interactivo y automático)
 ├── 🗑️ Desinstalador_Bot.py (Script para eliminar el bot del sistema)
 ├── 📄 README.md            (Este archivo)
 ├── 📄 .env                 (Generado automáticamente: Configuración)
 ├── 📄 config.json          (Generado automáticamente: Nombres y procesos)
 └── 📁 sistema/             (Archivos internos del bot)
      ├── 📄 requirements.txt
      ├── 📄 .env.example
      ├── 📁 core/           (Lógica interna del bot invisible para el usuario)
      └── 📁 assets/         (Iconos e imágenes)
```

---

### 2. Instalación Rápida (Recomendado)

Si prefieres una configuración guiada y visual:

1.  Descargar o clonar los archivos del repositorio.
2.  Ejecutar el asistente inicial con **doble clic** en:
    ```bash
    1_Instalar_Python.bat
    ```
    *(Este script comprobará si tienes Python instalado. Si no lo está, lo descargará e instalará automáticamente. Tras esto, se abrirá la ventana gráfica del Bot).*
3.  En la ventana que aparece, introduce tu **Token**, tu **ID** y personaliza los **nombres y rutas** de tus juegos y aplicaciones.
4.  (Opcional) Si necesitas instalar o reinstalar las librerías, asegúrate de marcar **"🔄 Reinstalar dependencias (pip install)"**.
5.  Pulsa en **"✅ GUARDAR CONFIG"**.
6.  Opciones de inicio rápido y atajos (puedes bajar con el scroll si no las ves):
    - **"🚀 AÑADIR A INICIO"**: Para agregar el bot al inicio de Windows.
    - **"❌ QUITAR DE INICIO"**: Para evitar que el bot arranque con Windows.
    - **"📌 CREAR EN ESCRITORIO"**: Para crear un acceso directo manual en tu escritorio.

---

### 3. Instalacion Manual (Usuarios Avanzados)

Si prefieres configurar los archivos manualmente o revisar el código interno:

1.  Descargar o clonar los archivos del repositorio.
2.  Instalar las dependencias necesarias:
    ```bash
    pip install -r sistema/requirements.txt
    ```
3.  Crear un archivo llamado `.env` en la carpeta raiz (basado en `.env.example`) y completar la informacion.
4.  Modificar el archivo `config.json` para cambiar los nombres de los botones en el menú de Telegram.
5.  Puedes arrancar el bot manualmente ejecutando `python sistema/core/bot.py`.


---

## Uso

Existen dos opciones para iniciar el bot:

- **Modo estandar**: Ejecutar `python sistema/core/bot.py`. Se abrira una ventana de consola.
- **Modo segundo plano (con icono en tray)**: Ejecutar `pythonw sistema/core/bot_tray.pyw`. El bot se ejecutara silenciosamente con un icono en la bandeja del sistema.

Una vez activo, enviar el comando `/start` al bot en Telegram para desplegar el menu interactivo.

---

## Desinstalación

Puedes eliminar completamente el bot, sus procesos y la carpeta entera usando cualquiera de estos métodos:

**Método 1: Desde el archivo principal**
1. Ejecuta el archivo `Desinstalador_Bot.py` que se encuentra en la carpeta principal del proyecto (`bot-telegram`).
2. Confirma la ventana de aviso y espera a que la consola termine de limpiar los archivos.

**Método 2: Desde la bandeja del sistema**
1.  Hacer **clic derecho** sobre el icono del bot en la bandeja del sistema (esquina inferior derecha de Windows).
2.  Seleccionar la opción **"Desinstalar aplicación"**.
3.  Confirmar la acción en la ventana emergente.

---

## Acceso rapido desde el movil

Para un control mas comodo, es recomendable añadir un acceso directo al chat del bot en la pantalla de inicio del movil.

### En Android
1. Abrir el chat del bot en Telegram.
2. Pulsar en el nombre del bot en la parte superior.
3. Pulsar en el icono de los tres puntos (Menu).
4. Seleccionar "Añadir a pantalla de inicio".

### En iOS (Shortcuts/Atajos)
1. Abrir la aplicacion "Atajos" (Shortcuts).
2. Crear un nuevo atajo pulsando en el "+".
3. Añadir la accion "Abrir URLs".
4. Escribir la URL del bot (ejemplo: `https://t.me/TuBotUsername`).
5. Pulsar en el icono de compartir y seleccionar "Añadir a pantalla de inicio".
6. Se puede personalizar el nombre y el icono (usando el logo del proyecto).

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
