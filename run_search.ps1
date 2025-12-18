# PowerShell script to run the Edge search automation
# This script handles the path spaces and virtual environment activation properly

Write-Host "Starting Edge Search Automation..." -ForegroundColor Green

# Get the script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Set paths with proper escaping
$PythonExe = Join-Path $ScriptDir ".venv\Scripts\python.exe"
$PythonScript = Join-Path $ScriptDir "search_trending_edge.py"

# Check if virtual environment exists
if (-not (Test-Path $PythonExe)) {
    Write-Host "Virtual environment not found. Please ensure .venv exists in the script directory." -ForegroundColor Red
    exit 1
}

# Check if the Python script exists
if (-not (Test-Path $PythonScript)) {
    Write-Host "search_trending_edge.py not found in the script directory." -ForegroundColor Red
    exit 1
}

Write-Host "Using Python: $PythonExe" -ForegroundColor Yellow
Write-Host "Running script: $PythonScript" -ForegroundColor Yellow

# Run the Python script with arguments passed to this script
try {
    & $PythonExe $PythonScript $args
    $exitCode = $LASTEXITCODE
    
    if ($exitCode -eq 0) {
        Write-Host "Script completed successfully!" -ForegroundColor Green
    } else {
        Write-Host "Script completed with exit code: $exitCode" -ForegroundColor Yellow
    }
} catch {
    Write-Host "Error running the script: $_" -ForegroundColor Red
    exit 1
}