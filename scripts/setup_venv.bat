@echo off
REM Context Engineering Lesson Setup - Windows
REM This script creates a virtual environment and installs dependencies
setlocal enabledelayedexpansion

echo ==================================
echo Context Engineering Lesson Setup
echo Windows Virtual Environment
echo ==================================
echo.

REM Function to check Python version (via label at end of file)
echo Searching for Python 3.12.x...

set "PYTHON_CMD="
set "PYTHON_VERSION="

REM Method 1: Check 'python' command
where python >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=2" %%v in ('python --version 2^>^&1') do set "PYTHON_VERSION=%%v"
    echo Checking python: !PYTHON_VERSION!
    echo !PYTHON_VERSION! | findstr /B "3.12." >nul
    if !errorlevel! equ 0 (
        set "PYTHON_CMD=python"
        echo [32mFound Python 3.12.x via 'python' command[0m
        goto :python_found
    )
)

REM Method 2: Check 'python3' command
where python3 >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=2" %%v in ('python3 --version 2^>^&1') do set "PYTHON_VERSION=%%v"
    echo Checking python3: !PYTHON_VERSION!
    echo !PYTHON_VERSION! | findstr /B "3.12." >nul
    if !errorlevel! equ 0 (
        set "PYTHON_CMD=python3"
        echo [32mFound Python 3.12.x via 'python3' command[0m
        goto :python_found
    )
)

REM Method 3: Check 'python3.12' command
where python3.12 >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=2" %%v in ('python3.12 --version 2^>^&1') do set "PYTHON_VERSION=%%v"
    echo Checking python3.12: !PYTHON_VERSION!
    echo !PYTHON_VERSION! | findstr /B "3.12." >nul
    if !errorlevel! equ 0 (
        set "PYTHON_CMD=python3.12"
        echo [32mFound Python 3.12.x via 'python3.12' command[0m
        goto :python_found
    )
)

REM Method 4: Check common installation paths
REM Check C:\Python312\python.exe
if exist "C:\Python312\python.exe" (
    for /f "tokens=2" %%v in ('"C:\Python312\python.exe" --version 2^>^&1') do set "PYTHON_VERSION=%%v"
    echo Checking C:\Python312\python.exe: !PYTHON_VERSION!
    echo !PYTHON_VERSION! | findstr /B "3.12." >nul
    if !errorlevel! equ 0 (
        set "PYTHON_CMD=C:\Python312\python.exe"
        echo [32mFound Python 3.12.x at C:\Python312\python.exe[0m
        goto :python_found
    )
)

REM Check %LOCALAPPDATA%\Programs\Python\Python312\python.exe
if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
    for /f "tokens=2" %%v in ('"%LOCALAPPDATA%\Programs\Python\Python312\python.exe" --version 2^>^&1') do set "PYTHON_VERSION=%%v"
    echo Checking %LOCALAPPDATA%\Programs\Python\Python312\python.exe: !PYTHON_VERSION!
    echo !PYTHON_VERSION! | findstr /B "3.12." >nul
    if !errorlevel! equ 0 (
        set "PYTHON_CMD=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
        echo [32mFound Python 3.12.x at %LOCALAPPDATA%\Programs\Python\Python312\python.exe[0m
        goto :python_found
    )
)

REM Check %APPDATA%\Python\Python312\python.exe
if exist "%APPDATA%\Python\Python312\python.exe" (
    for /f "tokens=2" %%v in ('"%APPDATA%\Python\Python312\python.exe" --version 2^>^&1') do set "PYTHON_VERSION=%%v"
    echo Checking %APPDATA%\Python\Python312\python.exe: !PYTHON_VERSION!
    echo !PYTHON_VERSION! | findstr /B "3.12." >nul
    if !errorlevel! equ 0 (
        set "PYTHON_CMD=%APPDATA%\Python\Python312\python.exe"
        echo [32mFound Python 3.12.x at %APPDATA%\Python\Python312\python.exe[0m
        goto :python_found
    )
)

REM Check C:\Program Files\Python312\python.exe
if exist "C:\Program Files\Python312\python.exe" (
    for /f "tokens=2" %%v in ('"C:\Program Files\Python312\python.exe" --version 2^>^&1') do set "PYTHON_VERSION=%%v"
    echo Checking C:\Program Files\Python312\python.exe: !PYTHON_VERSION!
    echo !PYTHON_VERSION! | findstr /B "3.12." >nul
    if !errorlevel! equ 0 (
        set "PYTHON_CMD=C:\Program Files\Python312\python.exe"
        echo [32mFound Python 3.12.x at C:\Program Files\Python312\python.exe[0m
        goto :python_found
    )
)

REM Check C:\Program Files (x86)\Python312\python.exe
if exist "C:\Program Files (x86)\Python312\python.exe" (
    for /f "tokens=2" %%v in ('"C:\Program Files (x86)\Python312\python.exe" --version 2^>^&1') do set "PYTHON_VERSION=%%v"
    echo Checking C:\Program Files (x86)\Python312\python.exe: !PYTHON_VERSION!
    echo !PYTHON_VERSION! | findstr /B "3.12." >nul
    if !errorlevel! equ 0 (
        set "PYTHON_CMD=C:\Program Files (x86)\Python312\python.exe"
        echo [32mFound Python 3.12.x at C:\Program Files (x86)\Python312\python.exe[0m
        goto :python_found
    )
)

REM Method 5: Try Python Launcher with -3.12 flag
where py >nul 2>&1
if %errorlevel% equ 0 (
    py -3.12 --version >nul 2>&1
    if !errorlevel! equ 0 (
        for /f "tokens=2" %%v in ('py -3.12 --version 2^>^&1') do set "PYTHON_VERSION=%%v"
        echo Checking py -3.12: !PYTHON_VERSION!
        echo !PYTHON_VERSION! | findstr /B "3.12." >nul
        if !errorlevel! equ 0 (
            set "PYTHON_CMD=py -3.12"
            echo [32mFound Python 3.12.x via Python Launcher (py -3.12)[0m
            goto :python_found
        )
    )
)

REM If we reach here, Python 3.12 was not found
echo.
echo [31m======================================================================[0m
echo [31m  Python 3.12.x Not Found - Installation Required[0m
echo [31m======================================================================[0m
echo.
echo Please install Python 3.12.x from:
echo   https://www.python.org/downloads/
echo.
echo Windows Installation Steps:
echo   1. Download the latest Python 3.12.x installer
echo   2. Run the installer
echo   3. [IMPORTANT] Check "Add Python to PATH"
echo   4. [OPTIONAL] Check "Install for all users"
echo   5. Complete the installation
echo   6. Restart your terminal
echo   7. Run this script again
echo.
echo Common installation locations to verify:
echo   - C:\Python312\
echo   - %%LOCALAPPDATA%%\Programs\Python\Python312\
echo.
pause
exit /b 1

:python_found
echo.
echo [32mUsing Python %PYTHON_VERSION%[0m
echo Command: %PYTHON_CMD%
echo.

REM Create virtual environment
echo.
echo Creating virtual environment (.venv)...
if exist .venv (
    echo .venv already exists, removing old environment...
    rmdir /s /q .venv
)

%PYTHON_CMD% -m venv .venv
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
%PYTHON_CMD% -m pip install --upgrade pip --quiet
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
%PYTHON_CMD% -c "import transformers; import torch; import sentence_transformers"
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
echo    python -m notebook notebooks\context_engineering_lesson.ipynb
echo.
pause
