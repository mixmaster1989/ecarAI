@echo off
echo Starting ИКАР-Ассистент 2.0 (Simplified Version)...
python simple_ikar.py
if %ERRORLEVEL% NEQ 0 (
    echo Error starting application. Please check the logs.
    pause
)