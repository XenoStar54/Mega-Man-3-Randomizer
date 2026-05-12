@echo off
setlocal

REM Build script for Mega-Man-3-Randomizer using PyInstaller
REM If a virtual environment exists in the project root, it will use that Python.
cd /d "%~dp0"
echo.
echo ===== Building mm3randomizer EXE =====

set "PYTHON=python"
if exist "%~dp0venv\Scripts\python.exe" (
    set "PYTHON=%~dp0venv\Scripts\python.exe"
)

if exist "%~dp0mm3randomizer.spec" (
    echo Using existing spec file: mm3randomizer.spec
    "%PYTHON%" -m PyInstaller --noconfirm --clean mm3randomizer.spec
) else (
    echo Spec file not found, building from script with PySide6 support.
    "%PYTHON%" -m PyInstaller --noconfirm --clean --windowed --icon=mm3.ico --hidden-import=PySide6.QtWidgets --hidden-import=PySide6.QtCore mm3randomizer.py
)

if errorlevel 1 (
    echo.
    echo Build failed. Please check the PyInstaller output for errors.
    pause
    exit /b 1
)

echo.
echo Build succeeded.
echo Output directory: dist\mm3randomizer
pause
