@echo off
title Europress SMART Material Value Engine - Cockpit Launcher
cd /d "%~dp0.."
python run_cockpit.py
if errorlevel 1 (
    echo.
    echo Launcher encountered an error. Press any key to exit.
    pause
)
