# PowerShell script to run automation with existing Edge browser
Write-Host "Setting up Edge for automation..." -ForegroundColor Green

# Get script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PythonExe = Join-Path $ScriptDir ".venv\Scripts\python.exe"
$PythonScript = Join-Path $ScriptDir "search_trending_edge.py"
$TestScript = Join-Path $ScriptDir "test_edge_connection.py"

# Check if files exist
if (-not (Test-Path $PythonExe)) {
    Write-Host "Python executable not found: $PythonExe" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $PythonScript)) {
    Write-Host "Main script not found: $PythonScript" -ForegroundColor Red
    exit 1
}

# Kill existing Edge processes
Write-Host "Closing existing Edge windows..." -ForegroundColor Yellow
Get-Process -Name "msedge" -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Seconds 3

# Find Edge executable
$edgePath = "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe"
if (-not (Test-Path $edgePath)) {
    $edgePath = "$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe"
}

if (-not (Test-Path $edgePath)) {
    Write-Host "Could not find Edge executable" -ForegroundColor Red
    Write-Host "Please start Edge manually: msedge.exe --remote-debugging-port=9222" -ForegroundColor Yellow
    exit 1
}

# Setup temp directory
$tempDir = Join-Path $env:TEMP "edge-automation"
if (-not (Test-Path $tempDir)) {
    New-Item -ItemType Directory -Path $tempDir -Force | Out-Null
}

# Start Edge with remote debugging
Write-Host "Starting Edge with remote debugging..." -ForegroundColor Yellow
$edgeArgs = "--remote-debugging-port=9222", "--user-data-dir=`"$tempDir`"", "--no-first-run", "--no-default-browser-check"
Start-Process -FilePath $edgePath -ArgumentList $edgeArgs
Start-Sleep -Seconds 5

# Test debugging port
Write-Host "Testing debugging port..." -ForegroundColor Yellow
try {
    $null = Invoke-WebRequest -Uri "http://127.0.0.1:9222/json" -TimeoutSec 5 -ErrorAction Stop
    Write-Host "✓ Edge debugging port is accessible" -ForegroundColor Green
} catch {
    Write-Host "✗ Edge debugging port not accessible" -ForegroundColor Red
    Write-Host "Trying to continue anyway..." -ForegroundColor Yellow
}

# Test basic connection
if (Test-Path $TestScript) {
    Write-Host "Testing Edge connection..." -ForegroundColor Yellow
    try {
        & $PythonExe $TestScript
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Edge connection test passed!" -ForegroundColor Green
        } else {
            Write-Host "✗ Edge connection test failed, but continuing..." -ForegroundColor Yellow
        }
    } catch {
        Write-Host "Connection test error: $_" -ForegroundColor Yellow
    }
}

# Run main automation script
Write-Host "Starting automation script..." -ForegroundColor Green
try {
    & $PythonExe $PythonScript --existing $args
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Script completed successfully!" -ForegroundColor Green
    } else {
        Write-Host "Script completed with exit code: $LASTEXITCODE" -ForegroundColor Yellow
    }
} catch {
    Write-Host "Script execution error: $_" -ForegroundColor Red
}

Write-Host "You can now use Edge normally." -ForegroundColor Green