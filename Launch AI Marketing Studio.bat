@echo off
title AI Marketing Studio
cd /d "%~dp0"

if not exist ".venv\Scripts\activate.bat" (
    echo.
    echo ERROR: Could not find the virtual environment folder ".venv"
    echo Make sure this launcher is placed in the same folder as main.py
    echo.
    pause
    exit /b 1
)

call .venv\Scripts\activate.bat

if not exist "main.py" (
    echo.
    echo ERROR: Could not find main.py in this folder.
    echo.
    pause
    exit /b 1
)

python main.py

if errorlevel 1 (
    echo.
    echo Something went wrong while running the app. See the error above.
    echo.
    pause
)