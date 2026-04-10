@echo off
title Asistente de Preparación - Bot XRD
chcp 65001 > nul

:: --- COMPROBACIÓN DE ADMINISTRADOR ---
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Se requieren permisos de Administrador.
    echo Por favor, haz clic derecho en este archivo y selecciona "Ejecutar como administrador".
    pause
    exit /b 1
)

echo ==============================================
echo   BOT DE TELEGRAM - ASISTENTE DE ENTORNO
echo ==============================================
echo.

:: --- COMPROBAR SI PYTHON YA ESTÁ ---
python --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] Python ya esta instalado y configurado correctamente.
    goto RUN_BOT
)

py --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] Python (Launcher) detectado.
    goto RUN_BOT
)

echo [INFO] Python NO se detecta en el sistema. Procediendo a la instalacion...
echo [ATENCION] Descargando el instalador oficial de Python (3.11.8)...
echo.

set PYTHON_URL=https://www.python.org/ftp/python/3.11.8/python-3.11.8-amd64.exe
set INSTALLER_PATH=%TEMP%\python_installer.exe

powershell -Command "Invoke-WebRequest -Uri '%PYTHON_URL%' -OutFile '%INSTALLER_PATH%'"

if not exist "%INSTALLER_PATH%" (
    echo [ERROR] No se pudo descargar el instalador. Revisa tu conexion.
    pause
    exit /b 1
)

echo [INFO] Instalando Python... Por favor espera a que termine la barra de progreso.
echo IMPORTANTE: Si Windows te pregunta, pulsa "SI" para permitir la instalacion.
echo.

:: /passive muestra barra de progreso pero no requiere clics extras (a menos que pida admin)
start /wait "" "%INSTALLER_PATH%" /passive InstallAllUsers=0 PrependPath=1 Include_test=0 Include_doc=0

if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] La instalacion de Python fallo o fue cancelada.
    pause
    exit /b 1
)

echo [OK] Instalacion de Python completada.
echo.

:: --- REFRESCAR PATH SIN REINICIAR CMD ---
:: Intentamos encontrar el ejecutable recien instalado
for /f "delims=" %%i in ('where python 2^>nul') do set "PY_PATH=%%i"
if not defined PY_PATH (
    if exist "%USERPROFILE%\AppData\Local\Programs\Python\Python311\python.exe" (
        set "PY_PATH=%USERPROFILE%\AppData\Local\Programs\Python\Python311\python.exe"
    ) else (
        echo [INFO] Refrescando variables de entorno...
        :: Pequeno truco para refrescar el PATH en la sesion actual
        for /f "tokens=2*" %%A in ('reg query "HKCU\Environment" /v Path') do set "PATH=%%B;%PATH%"
    )
)

:RUN_BOT
echo [INFO] Iniciando el configurador del Bot...
echo.

:: Intentamos lanzar con distintos alias
python Instalador_Bot.py 2>nul
if %ERRORLEVEL% NEQ 0 (
    py Instalador_Bot.py 2>nul
    if %ERRORLEVEL% NEQ 0 (
        "%PY_PATH%" Instalador_Bot.py 2>nul
        if %ERRORLEVEL% NEQ 0 (
            echo [ERROR] No se pudo lanzar el configurador automaticamente.
            echo Por favor, abre el archivo "Instalador_Bot.py" manualmente.
            pause
            exit /b 1
        )
    )
)

echo.
echo [OK] El configurador se ha cerrado.
pause
exit /b 0
