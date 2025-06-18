@echo off
echo Checking ИКАР-Ассистент status...
python check_status.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Issues detected. Please check the output above.
    pause
) else (
    echo.
    echo All systems operational!
    timeout /t 3
)