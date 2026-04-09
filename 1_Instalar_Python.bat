@echo off
title Preparando el entorno para el Bot...
chcp 65001 > nul

echo ==============================================
echo   BOT DE TELEGRAM - ASISTENTE DE ARRANQUE
echo ==============================================
echo.

:: Comprobar si Python esta instalado (mirando si python o py devuelve error)
python --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] Python ya esta instalado en el sistema.
    goto RUN_BOT
)

py --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] Python ya esta instalado en el sistema (Python Launcher).
    goto RUN_BOT
)

echo [INFO] Python NO esta instalado o no se encuentra en la variable PATH.
echo [ATENCION] Descargando el instalador oficial de Python (3.11.8)...
echo.
echo Esto puede tardar uno o dos minutos dependiendo de tu conexion...
echo.

set PYTHON_URL=https://www.python.org/ftp/python/3.11.8/python-3.11.8-amd64.exe
set INSTALLER_PATH=%TEMP%\python_installer.exe

powershell -Command "Invoke-WebRequest -Uri '%PYTHON_URL%' -OutFile '%INSTALLER_PATH%'"

if not exist "%INSTALLER_PATH%" (
    echo [ERROR] Hubo un problema al descargar el instalador de Python.
    echo Asegurate de estar conectado a Internet y vuelve a intentarlo.
    pause
    exit /b 1
)

echo [INFO] Instalando Python... Se pediran permisos de administrador. 
echo La instalacion es automatica y silenciosa (sin ventanas).
echo Por favor pulsa "SI" en la ventana de permisos si aparece.
echo.

:: Comando oficial para instalacion silenciosa
start /wait "" "%INSTALLER_PATH%" /quiet InstallAllUsers=0 PrependPath=1 Include_test=0 Include_doc=0

echo [OK] Instalacion de Python completada.

:RUN_BOT
echo.
echo [OK] Lanzando el instalador interactivo del Bot...
echo.

:: Python suele necesitar refrescar el CMD para reconocer el PATH. 
:: Probamos los metodos en orden para garantizar la ejecucion.
python Instalador_Bot.py 2>nul
if %ERRORLEVEL% NEQ 0 (
    py Instalador_Bot.py 2>nul
    if %ERRORLEVEL% NEQ 0 (
        "%USERPROFILE%\AppData\Local\Programs\Python\Python311\python.exe" Instalador_Bot.py 2>nul
        if %ERRORLEVEL% NEQ 0 (
            echo [ERROR] No se pudo lanzar el Bot de forma automatica. 
            echo Prueba a abrir manualmente el archivo "Instalador_Bot.py".
            pause
            exit /b 1
        )
    )
)

exit /b 0
