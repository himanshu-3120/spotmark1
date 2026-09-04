@echo off
title Push Spot Problem Solver to GitHub
cd /d "%~dp0"
echo ===========================================================
echo   Pushing Spot Problem Solver to GitHub
echo   Repository: https://github.com/himanshu-3120/spot-project.git
echo ===========================================================
echo.
git remote add origin https://github.com/himanshu-3120/spot-project.git 2>nul
git remote set-url origin https://github.com/himanshu-3120/spot-project.git
git branch -M main
git push -u origin main
echo.
echo Done! Press any key to exit.
pause
