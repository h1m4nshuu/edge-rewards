# Simple Microsoft Rewards automation - no prompts
Write-Host "Starting Microsoft Rewards automation..." -ForegroundColor Green

# Get script directory and paths
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PythonExe = Join-Path $ScriptDir ".venv\Scripts\python.exe"

# Check if Python exists
if (-not (Test-Path $PythonExe)) {
    Write-Host "Error: Python executable not found!" -ForegroundColor Red
    exit 1
}

# Close existing Edge processes
Write-Host "Closing existing Edge windows..." -ForegroundColor Yellow
Get-Process -Name "msedge" -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Seconds 2

# Find Edge executable
$EdgePath = "$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe"
if (-not (Test-Path $EdgePath)) {
    $EdgePath = "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe"
}

if (-not (Test-Path $EdgePath)) {
    Write-Host "Error: Edge executable not found!" -ForegroundColor Red
    exit 1
}

# Create temp directory
$TempDir = Join-Path $env:TEMP "edge-rewards"
New-Item -ItemType Directory -Path $TempDir -Force | Out-Null

# Start Edge with debugging
Write-Host "Starting Edge browser..." -ForegroundColor Yellow
$Arguments = @(
    "--remote-debugging-port=9222"
    "--user-data-dir=`"$TempDir`""
    "--no-first-run"
)

Start-Process -FilePath $EdgePath -ArgumentList $Arguments
Start-Sleep -Seconds 5

# Run automation
Write-Host "Starting search automation..." -ForegroundColor Green
Write-Host "Make sure you are signed into Microsoft account!" -ForegroundColor Yellow

try {
    & $PythonExe "search_trending_edge.py" --existing
    Write-Host "Automation completed successfully!" -ForegroundColor Green
} catch {
    Write-Host "Error running automation: $_" -ForegroundColor Red
    exit 1
}

Write-Host "Check rewards.microsoft.com for points earned" -ForegroundColor Cyan