@echo off
echo Setting up Edge for automation...

REM Kill any existing Edge processes
echo Closing existing Edge windows...
taskkill /f /im msedge.exe >nul 2>&1

REM Wait a moment for processes to close
timeout /t 2 >nul

REM Start Edge with remote debugging
echo Starting Edge with remote debugging...
start "" "msedge.exe" --remote-debugging-port=9222 --user-data-dir="%TEMP%\edge-automation"

REM Wait for Edge to start
echo Waiting for Edge to initialize...
timeout /t 3 >nul

REM Run the automation script
echo Starting automation script...
cd /d "%~dp0"
".venv\Scripts\python.exe" "search_trending_edge.py" --existing %*

echo.
echo Script completed. You can now use Edge normally.
pause