@echo off
title Building AI Marketing Studio
cd /d "%~dp0"

call .venv\Scripts\activate.bat

echo Installing PyInstaller if needed...
pip install pyinstaller

echo.
echo Building app... this may take a few minutes.
echo.

pyinstaller main.py ^
    --name "AI Marketing Studio" ^
    --onedir ^
    --windowed ^
    --noconfirm ^
    --collect-all playwright ^
    --collect-all PySide6 ^
    --collect-all cv2 ^
    --add-data "assets;assets" ^
    --add-data "templates;templates" ^
    --add-data "config;config"

echo.
echo Build finished. Your app is in the "dist\AI Marketing Studio" folder.
echo Look for "AI Marketing Studio.exe" inside it.
echo.
pause