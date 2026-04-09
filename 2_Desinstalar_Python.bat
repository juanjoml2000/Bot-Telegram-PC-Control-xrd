@echo off
title Desinstalador de Python 3.11.8
chcp 65001 > nul

echo ==============================================
echo       DESINSTALADOR SILENCIOSO DE PYTHON
echo ==============================================
echo.
echo NOTA: Si ya tenias otra version de Python instalada antes, 
echo esta operacion podria no ser necesaria. Esto borrara la version
echo 3.11.8 que este script instalo originalmente.
echo.
pause

set INSTALLER_PATH=%TEMP%\python_installer.exe
set PYTHON_URL=https://www.python.org/ftp/python/3.11.8/python-3.11.8-amd64.exe

if not exist "%INSTALLER_PATH%" (
    echo [INFO] Descargando el desinstalador temporalmente...
    powershell -Command "Invoke-WebRequest -Uri '%PYTHON_URL%' -OutFile '%INSTALLER_PATH%'"
)

echo.
echo [INFO] Desinstalando Python silenciosamente...
start /wait "" "%INSTALLER_PATH%" /uninstall /quiet

echo.
echo [OK] Operacion completada. Revisa la lista de programas de Windows
echo si quieres confirmar que Python se ha desinstalado completamente.
echo.
pause
