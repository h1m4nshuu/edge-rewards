# Simple test with NEW browser window (won't interfere with your browsing)
Write-Host "Testing with NEW Edge browser window..." -ForegroundColor Green

# Get script directory and paths
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PythonExe = Join-Path $ScriptDir ".venv\Scripts\python.exe"

Write-Host "This opens a completely separate Edge browser for testing" -ForegroundColor Yellow
Write-Host "Your regular browsing is not affected!" -ForegroundColor Green
Write-Host ""

# Create simple test script for NEW browser (not existing)
$TestCode = @"
import sys
import os
sys.path.append(r'$ScriptDir')

# Import the main functions
from search_trending_edge import run_search_sequence

# Generate different test topics each time
import random
import datetime

def generate_test_topics():
    current_time = datetime.datetime.now()
    
    topic_pools = [
        # Current events with time stamps
        [f"news {current_time.strftime('%B %d')}", f"weather {current_time.strftime('%A')}", f"events today"],
        
        # Technology topics
        ["artificial intelligence news", "latest smartphone", "tech innovations", "software updates", "gaming news"],
        
        # Lifestyle topics  
        ["healthy recipes", "fitness tips", "travel destinations", "home improvement", "fashion trends"],
        
        # Entertainment
        ["movie reviews", "music charts", "TV shows", "celebrity news", "streaming recommendations"],
        
        # Educational
        ["how to learn", "study methods", "online courses", "skill development", "career advice"]
    ]
    
    # Pick one topic from each pool randomly
    test_topics = []
    for pool in topic_pools[:3]:  # Only take 3 for testing
        topic = random.choice(pool)
        # Add some variation
        modifiers = ["latest", "best", "top", "new", "trending", "2024", "guide", "tips"]
        if random.random() < 0.5:
            topic = f"{random.choice(modifiers)} {topic}"
        test_topics.append(topic)
    
    return test_topics

test_topics = generate_test_topics()

print("Starting test with NEW browser window (3 searches)...")
print("This will not interfere with your regular Edge browsing.")
print(f"Today's test topics: {test_topics}")
print()

try:
    # use_existing=False means it opens a NEW browser window
    run_search_sequence(test_topics, headless=False, min_wait=8, max_wait=12, use_existing=False)
    print()
    print("✅ NEW browser test completed successfully!")
    print("The automation browser will close automatically.")
except Exception as e:
    print(f"❌ Test failed: {e}")
"@

$TestScriptPath = Join-Path $ScriptDir "new_browser_test.py"
$TestCode | Out-File -FilePath $TestScriptPath -Encoding UTF8

Write-Host "Starting test..." -ForegroundColor Green
& $PythonExe $TestScriptPath

Write-Host "Test completed!" -ForegroundColor Green