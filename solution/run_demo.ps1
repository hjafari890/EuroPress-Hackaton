# Europress SMART Material Value Engine — One-Click Demo Launcher
$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $RepoRoot

Write-Host "=================================================================" -ForegroundColor Red
Write-Host " EUROPRESS SMART MATERIAL VALUE ENGINE — HACKATHON DEMO LAUNCHER " -ForegroundColor White
Write-Host "=================================================================" -ForegroundColor Red

if (-not (Test-Path "$RepoRoot\solution\backend\data\cockpit_bundle.json")) {
    Write-Host "[1/2] Generating Cockpit Data Bundle from Competition Dataset..." -ForegroundColor Yellow
    python "$RepoRoot\solution\engine\export_cockpit_data.py"
} else {
    Write-Host "[1/2] Verified pre-computed Cockpit Data Bundle (solution\backend\data\cockpit_bundle.json)." -ForegroundColor Green
}

Write-Host "[2/2] Starting FastAPI + Europress SMART Web Cockpit at http://localhost:8000 ..." -ForegroundColor Cyan
Write-Host "      Open http://localhost:8000 in your browser (Ctrl+C to stop)." -ForegroundColor Green
python -m uvicorn solution.backend.app:app --host 127.0.0.1 --port 8000
