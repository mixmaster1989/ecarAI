@echo off
echo Starting ИКАР-Ассистент 2.0...

:: Run the complete batch file with error handling
call run_ikar_complete.bat
exit /b %ERRORLEVEL%