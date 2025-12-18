# Standalone Microsoft Rewards automation - opens its OWN browser
Write-Host "Microsoft Rewards Standalone Automation" -ForegroundColor Green
Write-Host "=======================================" -ForegroundColor Green

# Get script directory and paths
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PythonExe = Join-Path $ScriptDir ".venv\Scripts\python.exe"

# Check if Python exists
if (-not (Test-Path $PythonExe)) {
    Write-Host "Error: Python executable not found!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "This will open a SEPARATE Edge browser just for automation" -ForegroundColor Cyan
Write-Host "Your regular browsing will NOT be affected!" -ForegroundColor Green
Write-Host ""
Write-Host "IMPORTANT:" -ForegroundColor Yellow
Write-Host "- Sign into Microsoft account in your regular Edge browser first" -ForegroundColor White
Write-Host "- This automation will use a separate browser window" -ForegroundColor White
Write-Host "- Do NOT close the automation browser window until complete" -ForegroundColor White
Write-Host ""

$response = Read-Host "Ready to start standalone automation? (y/n)"
if ($response -ne 'y' -and $response -ne 'Y') {
    Write-Host "Automation cancelled." -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "Starting standalone Edge browser for automation..." -ForegroundColor Green

# Run automation with NEW browser (not existing one)
try {
    & $PythonExe "search_trending_edge.py"
    Write-Host ""
    Write-Host "Standalone automation completed successfully!" -ForegroundColor Green
} catch {
    Write-Host "Error running automation: $_" -ForegroundColor Red
    exit 1
}

Write-Host "Check rewards.microsoft.com for points earned" -ForegroundColor Cyan
Write-Host "Points may take a few minutes to appear" -ForegroundColor Yellow