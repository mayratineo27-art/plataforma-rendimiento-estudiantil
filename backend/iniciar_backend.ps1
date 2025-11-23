# ===================================================================
# Script para iniciar el Backend en PowerShell
# ===================================================================

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  INICIANDO BACKEND - Plataforma de Rendimiento Estudiantil  ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Cambiar al directorio del script
Set-Location $PSScriptRoot

# Verificar si existe el entorno virtual
if (-not (Test-Path "venv")) {
    Write-Host "[ERROR] No se encontró el entorno virtual 'venv'" -ForegroundColor Red
    Write-Host "Por favor, ejecuta primero:" -ForegroundColor Yellow
    Write-Host "  python -m venv venv" -ForegroundColor White
    Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor White
    Write-Host "  pip install -r requirements.txt" -ForegroundColor White
    pause
    exit 1
}

# Activar entorno virtual
Write-Host "[1/3] Activando entorno virtual..." -ForegroundColor Green
& ".\venv\Scripts\Activate.ps1"

# Verificar variables de entorno
Write-Host "[2/3] Verificando configuración..." -ForegroundColor Green
if (-not (Test-Path ".env")) {
    Write-Host "[ADVERTENCIA] No se encontró el archivo .env" -ForegroundColor Yellow
    Write-Host "Usando configuración por defecto" -ForegroundColor Yellow
}

# Iniciar el servidor Flask
Write-Host "[3/3] Iniciando servidor Flask..." -ForegroundColor Green
Write-Host ""
python run.py

# Si el servidor se detiene
Write-Host ""
Write-Host "[INFO] Servidor detenido" -ForegroundColor Cyan
pause
