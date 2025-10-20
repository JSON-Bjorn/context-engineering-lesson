@echo off
REM Context Engineering Lesson Setup - Windows
REM This script creates a virtual environment and installs dependencies

echo ==================================
echo Context Engineering Lesson Setup
echo Windows Virtual Environment
echo ==================================
echo.

REM Check for Python 3.12
echo Checking for Python 3.12...
python --version 2>&1 | findstr /C:"3.12" >nul
if %errorlevel% neq 0 (
    echo Error: Python 3.12 required
    echo Please install Python 3.12 from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)
echo Found Python 3.12

REM Create virtual environment
echo.
echo Creating virtual environment (.venv)...
if exist .venv (
    echo .venv already exists, removing old environment...
    rmdir /s /q .venv
)

python -m venv .venv
if %errorlevel% neq 0 (
    echo Error: Failed to create virtual environment
    pause
    exit /b 1
)
echo Virtual environment created

REM Activate virtual environment
echo.
echo Activating virtual environment...
call .venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo Error: Failed to activate virtual environment
    pause
    exit /b 1
)
echo Virtual environment activated

REM Upgrade pip
echo.
echo Upgrading pip...
python -m pip install --upgrade pip --quiet
echo pip upgraded

REM Install dependencies
echo.
echo Installing dependencies (this may take 3-5 minutes)...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)
echo Dependencies installed

REM Verify installation
echo.
echo Verifying installation...
python -c "import transformers; import torch; import sentence_transformers"
if %errorlevel% neq 0 (
    echo Error: Package verification failed
    pause
    exit /b 1
)
echo All critical packages installed successfully

REM Success message
echo.
echo ==================================
echo Setup Complete!
echo ==================================
echo.
echo Next steps:
echo 1. Activate the environment:
echo    .venv\Scripts\activate.bat
echo.
echo 2. Start the lesson:
echo    jupyter notebook notebooks\context_engineering_lesson.ipynb
echo.
pause
