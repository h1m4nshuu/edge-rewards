# PowerShell script to run automation with existing Edge browser
Write-Host "Setting up Edge for automation..." -ForegroundColor Green

# Get script directory and paths
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PythonExe = Join-Path $ScriptDir ".venv\Scripts\python.exe"
$PythonScript = Join-Path $ScriptDir "search_trending_edge.py"

# Check if Python exists
if (-not (Test-Path $PythonExe)) {
    Write-Host "Python executable not found!" -ForegroundColor Red
    exit 1
}

# Close existing Edge processes
Write-Host "Closing existing Edge windows..." -ForegroundColor Yellow
Get-Process -Name "msedge" -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Seconds 2

# Find Edge executable
$EdgePath = "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe"
if (-not (Test-Path $EdgePath)) {
    $EdgePath = "$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe"
}

if (-not (Test-Path $EdgePath)) {
    Write-Host "Edge executable not found!" -ForegroundColor Red
    exit 1
}

# Create temp directory for Edge
$TempDir = Join-Path $env:TEMP "edge-automation"
New-Item -ItemType Directory -Path $TempDir -Force | Out-Null

# Start Edge with debugging
Write-Host "Starting Edge with debugging..." -ForegroundColor Yellow
$Arguments = @(
    "--remote-debugging-port=9222"
    "--user-data-dir=`"$TempDir`""
    "--no-first-run"
)

Start-Process -FilePath $EdgePath -ArgumentList $Arguments
Write-Host "Waiting for Edge to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 6

# Important warning
Write-Host "IMPORTANT: Do NOT close the Edge browser window during automation!" -ForegroundColor Red
Write-Host "The automation will control the browser automatically." -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop the script if needed." -ForegroundColor Yellow
Write-Host ""
Start-Sleep -Seconds 2

# Run the automation script
Write-Host "Starting automation..." -ForegroundColor Green
& $PythonExe $PythonScript --existing

Write-Host "Automation completed!" -ForegroundColor Green