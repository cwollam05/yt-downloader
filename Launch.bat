@echo off
cd /d "%~dp0"

:: Check Python is available
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found. Please make sure Python is installed.
    pause
    exit /b 1
)

:: Open the browser after a short delay (runs separately)
start "" cmd /c "timeout /t 2 /nobreak >nul && start http://localhost:5000"

:: Start the server (keeps this window open — close it to stop the server)
echo Starting YouTube Downloader...
echo Close this window to stop the server.
echo.
python server.py
