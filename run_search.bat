@echo off
echo Starting Edge Search Automation...

REM Change to script directory
cd /d "%~dp0"

REM Check if virtual environment exists
if not exist ".venv\Scripts\python.exe" (
    echo Virtual environment not found. Please ensure .venv exists.
    pause
    exit /b 1
)

REM Run the Python script
".venv\Scripts\python.exe" "search_trending_edge.py" %*

REM Check exit code
if %ERRORLEVEL% EQU 0 (
    echo Script completed successfully!
) else (
    echo Script completed with error code: %ERRORLEVEL%
)

pause