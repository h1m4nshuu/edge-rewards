# PowerShell script optimized for Microsoft Rewards points
Write-Host "Microsoft Rewards Point Optimizer" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green

# Get script directory and paths
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PythonExe = Join-Path $ScriptDir ".venv\Scripts\python.exe"

# Check if Python exists
if (-not (Test-Path $PythonExe)) {
    Write-Host "Python executable not found!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "IMPORTANT SETUP FOR MICROSOFT REWARDS:" -ForegroundColor Yellow
Write-Host "1. Make sure you're signed into your Microsoft account in Edge" -ForegroundColor White
Write-Host "2. Visit bing.com first to confirm you're logged in" -ForegroundColor White
Write-Host "3. Check that Microsoft Rewards is available in your region" -ForegroundColor White
Write-Host "4. Do NOT close the browser window during automation" -ForegroundColor White
Write-Host ""

Write-Host "This script will:" -ForegroundColor Cyan
Write-Host "- Perform human-like searches with realistic typing and clicking" -ForegroundColor White
Write-Host "- Include engagement actions (result clicks, tab switches)" -ForegroundColor White  
Write-Host "- Add search variations to maximize uniqueness" -ForegroundColor White
Write-Host "- Use optimal timing for reward point qualification" -ForegroundColor White
Write-Host ""

$response = Read-Host "Are you signed into Microsoft account and ready to start? (y/n)"
if ($response -ne 'y' -and $response -ne 'Y') {
    Write-Host "Please sign into your Microsoft account first, then run this script again." -ForegroundColor Yellow
    exit 0
}

# Close existing Edge processes
Write-Host "Preparing Edge browser..." -ForegroundColor Yellow
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
$TempDir = Join-Path $env:TEMP "edge-rewards-automation"
New-Item -ItemType Directory -Path $TempDir -Force | Out-Null

# Start Edge with debugging
Write-Host "Starting Edge with rewards optimization..." -ForegroundColor Yellow
$Arguments = @(
    "--remote-debugging-port=9222"
    "--user-data-dir=`"$TempDir`""
    "--no-first-run"
    "--disable-default-browser-check"
)

Start-Process -FilePath $EdgePath -ArgumentList $Arguments
Write-Host "Waiting for Edge to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 6

Write-Host ""
Write-Host "CRITICAL: The Edge window that just opened is for automation only!" -ForegroundColor Red
Write-Host "Do NOT close it until the script completes!" -ForegroundColor Red
Write-Host ""
Write-Host "Starting Microsoft Rewards search automation..." -ForegroundColor Green

# Create rewards-optimized Python script
$RewardsCode = @"
import sys
import os
sys.path.append(r'$ScriptDir')

# Import the main functions  
from search_trending_edge import run_search_sequence

# Microsoft Rewards optimized search topics
rewards_topics = [
    "weather forecast today",
    "breaking news headlines", 
    "best restaurants near me",
    "movie reviews 2024",
    "healthy recipe ideas",
    "technology news updates", 
    "travel destinations 2024",
    "fitness workout tips",
    "stock market today",
    "sports scores updates",
    "celebrity news latest",
    "fashion trends 2024", 
    "home improvement ideas",
    "car reviews 2024",
    "gaming news updates",
    "music charts today",
    "book recommendations",
    "science discoveries 2024",
    "history facts interesting",
    "art gallery exhibitions",
    "photography tips beginner",
    "cooking techniques basic",
    "gardening tips seasonal",
    "pet care advice",
    "education courses online",
    "job market trends",
    "real estate prices", 
    "cryptocurrency news",
    "climate change updates",
    "space exploration news"
]

print("Starting Microsoft Rewards optimized automation...")
print("This will perform 30 unique searches with maximum reward qualification")
print()

try:
    run_search_sequence(rewards_topics, headless=False, min_wait=20, max_wait=35, use_existing=True)
    print()
    print("🎉 Microsoft Rewards automation completed!")
    print("Check your Microsoft Rewards dashboard to confirm points earned.")
except Exception as e:
    print(f"❌ Automation failed: {e}")
"@

$RewardsScriptPath = Join-Path $ScriptDir "rewards_automation.py"
$RewardsCode | Out-File -FilePath $RewardsScriptPath -Encoding UTF8

# Run the rewards automation
& $PythonExe $RewardsScriptPath

Write-Host ""
Write-Host "🏆 Microsoft Rewards automation completed!" -ForegroundColor Green
Write-Host "💡 Check your Microsoft Rewards dashboard at rewards.microsoft.com" -ForegroundColor Cyan
Write-Host "📊 Points may take a few minutes to appear in your account" -ForegroundColor Yellow