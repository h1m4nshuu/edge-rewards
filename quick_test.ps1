# PowerShell script for testing with just 5 searches
Write-Host "Testing Edge automation with 5 searches only..." -ForegroundColor Green

# Get script directory and paths
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PythonExe = Join-Path $ScriptDir ".venv\Scripts\python.exe"

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
$TempDir = Join-Path $env:TEMP "edge-automation-test"
New-Item -ItemType Directory -Path $TempDir -Force | Out-Null

# Start Edge with debugging
Write-Host "Starting Edge with debugging..." -ForegroundColor Yellow
$Arguments = @(
    "--remote-debugging-port=9222"
    "--user-data-dir=`"$TempDir`""
    "--no-first-run"
)

Start-Process -FilePath $EdgePath -ArgumentList $Arguments
Write-Host "Edge started. Waiting 6 seconds..." -ForegroundColor Yellow
Start-Sleep -Seconds 6

Write-Host "IMPORTANT: Do NOT close the Edge browser window!" -ForegroundColor Red
Write-Host "Starting test with 5 searches only..." -ForegroundColor Green

# Create a test script with only 5 topics
$TestCode = @"
import sys
import os
sys.path.append(r'$ScriptDir')

# Import the main functions
from search_trending_edge import run_search_sequence

# Generate different test topics each time
import random
import datetime

current_time = datetime.datetime.now()
day_of_week = current_time.strftime('%A')
month = current_time.strftime('%B')

# Dynamic test topics that change based on time
dynamic_topics = [
    f"weather forecast {day_of_week}",
    f"trending news {month} 2024", 
    f"best {random.choice(['restaurants', 'movies', 'books', 'apps', 'games'])} near me",
    f"{random.choice(['latest', 'top', 'best', 'new'])} technology {random.choice(['news', 'updates', 'trends', 'innovations'])}",
    f"how to {random.choice(['learn', 'improve', 'master', 'start'])} {random.choice(['programming', 'cooking', 'fitness', 'photography', 'writing'])}",
    f"{random.choice(['healthy', 'quick', 'easy', 'delicious'])} {random.choice(['recipes', 'meals', 'snacks', 'breakfast'])}"
]

# Select 3 random topics for this test
test_topics = random.sample(dynamic_topics, 3)

print("Starting human-like behavior test with 3 searches...")
print("This test will demonstrate:")
print("- Human-like typing with realistic delays")
print("- Mouse movements and clicks")  
print("- Reading simulation with natural scrolling")
print("- Realistic pauses between actions")
print(f"Today's dynamic test topics: {test_topics}")
print()
try:
    run_search_sequence(test_topics, headless=False, min_wait=10, max_wait=15, use_existing=True)
    print("Human-like behavior test completed successfully!")
except Exception as e:
    print(f"Test failed: {e}")
"@

$TestScriptPath = Join-Path $ScriptDir "quick_test.py"
$TestCode | Out-File -FilePath $TestScriptPath -Encoding UTF8

# Run the test
& $PythonExe $TestScriptPath

Write-Host "Test completed!" -ForegroundColor Green