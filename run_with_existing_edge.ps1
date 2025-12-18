# PowerShell script to run automation with existing Edge browser
Write-Host "Setting up Edge for automation..." -ForegroundColor Green

# Get script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PythonExe = Join-Path $ScriptDir ".venv\Scripts\python.exe"
$PythonScript = Join-Path $ScriptDir "search_trending_edge.py"

# Kill existing Edge processes
Write-Host "Closing existing Edge windows..." -ForegroundColor Yellow
try {
    Get-Process -Name "msedge" -ErrorAction SilentlyContinue | Stop-Process -Force
    Write-Host "Closed existing Edge processes" -ForegroundColor Yellow
} catch {
    Write-Host "No existing Edge processes found" -ForegroundColor Yellow
}

# Wait for processes to close completely
Write-Host "Waiting for processes to close..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

# Find Edge executable
$edgePath = "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe"
if (-not (Test-Path $edgePath)) {
    $edgePath = "$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe"
}

if (-not (Test-Path $edgePath)) {
    Write-Host "Could not find Edge executable in standard locations" -ForegroundColor Red
    Write-Host "Please start Edge manually with: msedge.exe --remote-debugging-port=9222" -ForegroundColor Yellow
    exit 1
}

# Start Edge with remote debugging
Write-Host "Starting Edge with remote debugging..." -ForegroundColor Yellow
$tempDir = Join-Path $env:TEMP "edge-automation"

# Create the temp directory if it doesn't exist
if (-not (Test-Path $tempDir)) {
    New-Item -ItemType Directory -Path $tempDir -Force | Out-Null
}

# Start Edge process
$edgeArgs = @(
    "--remote-debugging-port=9222"
    "--user-data-dir=`"$tempDir`""
    "--no-first-run"
    "--no-default-browser-check"
)

Write-Host "Starting: $edgePath with debugging port 9222" -ForegroundColor Yellow
Start-Process -FilePath $edgePath -ArgumentList $edgeArgs

# Wait and verify Edge started with debugging
Write-Host "Waiting for Edge to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Test if debugging port is accessible
Write-Host "Testing debugging port accessibility..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:9222/json" -TimeoutSec 5 -ErrorAction Stop
    Write-Host "✓ Edge debugging port is accessible" -ForegroundColor Green
} catch {
    Write-Host "✗ Could not access Edge debugging port" -ForegroundColor Red
    Write-Host "Please manually start Edge with: msedge.exe --remote-debugging-port=9222" -ForegroundColor Yellow
    exit 1
}

# Test connection first
Write-Host "Testing Edge connection..." -ForegroundColor Yellow
$testScript = Join-Path $ScriptDir "test_edge_connection.py"
try {
    & $PythonExe $testScript
    $testResult = $LASTEXITCODE
    
    if ($testResult -eq 0) {
        Write-Host "✓ Edge connection test passed!" -ForegroundColor Green
        
        # Run the automation script
        Write-Host "Starting automation script..." -ForegroundColor Green
        & $PythonExe $PythonScript --existing $args
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Script completed successfully!" -ForegroundColor Green
        } else {
            Write-Host "Script completed with errors." -ForegroundColor Yellow
        }
    } else {
        Write-Host "✗ Edge connection test failed. Please check Edge setup." -ForegroundColor Red
    }
} catch {
    Write-Host "Error during execution: $_" -ForegroundColor Red
}

Write-Host "You can now use Edge normally." -ForegroundColor Green