@echo off
title RL Agentic System Launcher
color 0A

echo ========================================
echo    RL AGENTIC SYSTEM - LAUNCHER
echo ========================================
echo.
echo 1. Launch HTML Demo Only
echo 2. Run Python Implementation Only
echo 3. Run Full System (Both)
echo 4. Install Requirements
echo 5. Open Project in VS Code
echo 6. Generate Reports
echo 7. Exit
echo.

set /p choice="Select option (1-7): "

if %choice%==1 (
    echo Launching HTML Demo...
    start web_demo\rl_demo.html
    echo Demo launched in browser!
    pause
    start.bat
)

if %choice%==2 (
    echo Running Python Implementation...
    python main.py
    pause
    start.bat
)

if %choice%==3 (
    echo Launching Complete System...
    start web_demo\rl_demo.html
    timeout /t 2
    python main.py
    pause
    start.bat
)

if %choice%==4 (
    echo Installing Requirements...
    pip install -r requirements.txt
    echo Installation complete!
    pause
    start.bat
)

if %choice%==5 (
    echo Opening in VS Code...
    code .
    exit
)

if %choice%==6 (
    echo Generating Reports...
    python compare_implementations.py
    pause
    start.bat
)

if %choice%==7 (
    exit
)