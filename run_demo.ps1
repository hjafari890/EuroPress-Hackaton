# Europress SMART Material Value Engine — One-Click Demo Launcher
$ErrorActionPreference = "Stop"
$RepoRoot = $PSScriptRoot
Set-Location $RepoRoot

Write-Host "=================================================================" -ForegroundColor Red
Write-Host " EUROPRESS SMART MATERIAL VALUE ENGINE — HACKATHON DEMO LAUNCHER " -ForegroundColor White
Write-Host "=================================================================" -ForegroundColor Red

python run_cockpit.py
