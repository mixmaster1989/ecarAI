@echo off
echo Starting ИКАР-Ассистент 2.0...

:: Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed or not in PATH. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

:: Check if requirements are installed
echo Checking dependencies...
python -c "import sys, pkg_resources; pkg_resources.require(open('requirements.txt').readlines())" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Installing dependencies from requirements.txt...
    pip install -r requirements.txt
    if %ERRORLEVEL% NEQ 0 (
        echo Failed to install dependencies. Please check your internet connection and try again.
        pause
        exit /b 1
    )
)

:: Create necessary directories
echo Creating directory structure...
python create_dirs.py

:: Run the application
echo Starting application...
python run_ikar.py

if %ERRORLEVEL% NEQ 0 (
    echo Error starting application. Please check the logs.
    pause
)