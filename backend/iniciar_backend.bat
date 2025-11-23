@echo off
REM ===================================================================
REM Script para iniciar el Backend de la Plataforma de Rendimiento
REM ===================================================================

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║  INICIANDO BACKEND - Plataforma de Rendimiento Estudiantil  ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM Cambiar al directorio del backend
cd /d "%~dp0"

REM Verificar si existe el entorno virtual
if not exist "venv" (
    echo [ERROR] No se encontró el entorno virtual 'venv'
    echo Por favor, ejecuta primero: python -m venv venv
    echo Y luego: venv\Scripts\activate.bat
    echo Y después: pip install -r requirements.txt
    pause
    exit /b 1
)

REM Activar entorno virtual
echo [1/3] Activando entorno virtual...
call venv\Scripts\activate.bat

REM Verificar variables de entorno
echo [2/3] Verificando configuración...
if not exist ".env" (
    echo [ADVERTENCIA] No se encontró el archivo .env
    echo Usando configuración por defecto
)

REM Iniciar el servidor Flask
echo [3/3] Iniciando servidor Flask...
echo.
python run.py

REM Si el servidor se detiene
echo.
echo [INFO] Servidor detenido
pause
