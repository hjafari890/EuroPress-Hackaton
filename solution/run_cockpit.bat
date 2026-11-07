@echo off
title Europress SMART Material Value Engine - Cockpit Launcher
echo =====================================================================
echo  EUROPRESS SMART MATERIAL VALUE ENGINE - SINCE AI HACKATHON 2026
echo =====================================================================
echo.
echo Starting FastAPI Backend & Cockpit UI on http://localhost:8000 ...
echo.
start http://localhost:8000
python -m uvicorn solution.backend.app:app --host 0.0.0.0 --port 8000
pause
