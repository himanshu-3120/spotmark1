@echo off
title Spot Problem Solver Platform Launcher
echo ===========================================================
echo   SPOT PROBLEM SOLVER — Launching Web Platform...
echo   Tagline: "Spot a Problem. Build a Solution. Create an Impact."
echo ===========================================================
echo.
cd /d "%~dp0"
echo [1/2] Checking database...
python database.py
echo.
echo [2/2] Starting server at http://127.0.0.1:5000 ...
start "" "http://127.0.0.1:5000"
python app.py
pause
