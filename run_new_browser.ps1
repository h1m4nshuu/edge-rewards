# PowerShell script that creates a NEW Edge browser specifically for automation
Write-Host "Starting Edge automation with NEW browser window..." -ForegroundColor Green

# Get script directory and paths
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PythonExe = Join-Path $ScriptDir ".venv\Scripts\python.exe"
$PythonScript = Join-Path $ScriptDir "search_trending_edge.py"

# Check if Python exists
if (-not (Test-Path $PythonExe)) {
    Write-Host "Python executable not found!" -ForegroundColor Red
    exit 1
}

Write-Host "This will open a NEW Edge browser window for automation" -ForegroundColor Yellow
Write-Host "Do NOT close this browser window during automation!" -ForegroundColor Red
Write-Host "Press any key to start..." -ForegroundColor Green
Read-Host

# Run automation with NEW browser (not existing)
Write-Host "Starting automation with new browser..." -ForegroundColor Green
& $PythonExe $PythonScript

Write-Host "Automation completed!" -ForegroundColor Green