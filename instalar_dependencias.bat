@echo off
setlocal
cd /d "%~dp0"

echo Instalando dependencias de Hospital Financiero...
echo.
echo Buscando Python 3.12 o superior...

set "PYTHON_CMD="

py -3.12 -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 12) else 1)" >nul 2>&1
if %errorlevel%==0 set "PYTHON_CMD=py -3.12"

if "%PYTHON_CMD%"=="" (
    python -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 12) else 1)" >nul 2>&1
    if %errorlevel%==0 set "PYTHON_CMD=python"
)

if "%PYTHON_CMD%"=="" (
    echo No se encontro Python 3.12 o superior.
    echo Instala Python 3.12 desde https://www.python.org/downloads/
    echo Marca la opcion "Add python.exe to PATH" durante la instalacion.
    pause
    exit /b 1
)

echo Usando:
%PYTHON_CMD% --version
echo.

%PYTHON_CMD% -m ensurepip --upgrade
%PYTHON_CMD% -m pip install --upgrade pip
%PYTHON_CMD% -m pip install -r "%~dp0requirements.txt"

if errorlevel 1 (
    echo.
    echo Hubo un error instalando dependencias.
    pause
    exit /b 1
)

echo.
echo Listo. Las librerias ya instaladas se mantienen y pip instala las faltantes.
echo Ahora puedes abrir iniciar_escritorio.bat o iniciar_web_local.bat
pause
