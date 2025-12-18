# Topic Variety Showcase - Shows how dynamic topics work
Write-Host "🎯 TOPIC VARIETY SHOWCASE" -ForegroundColor Magenta
Write-Host "This shows how the dynamic topic generator creates unique searches" -ForegroundColor Yellow

# Get script directory and paths
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PythonExe = Join-Path $ScriptDir ".venv\Scripts\python.exe"

# Create variety showcase script
$ShowcaseCode = @"
import sys
import os
import random
import datetime
sys.path.append(r'$ScriptDir')

from search_trending_edge import generate_dynamic_topics

print("🎲 TOPIC GENERATION SHOWCASE")
print("=" * 60)
print()

# Show how topics change over multiple runs
print("📊 VARIETY DEMONSTRATION - 5 Different Runs:")
print("-" * 40)
for run in range(1, 6):
    topics = generate_dynamic_topics(4)
    print(f"Run {run}: {topics}")

print()
print("🕒 TIME-BASED TOPICS:")
print("-" * 40)

# Show time-based variation
current_time = datetime.datetime.now()
time_topics = [
    f"news update {current_time.strftime('%H:%M')}",
    f"trending now {current_time.strftime('%m-%d')}",
    f"breaking news hour {current_time.hour}",
    f"latest updates minute {current_time.minute}",
    f"current events day {current_time.day}"
]
for topic in time_topics:
    print(f"  • {topic}")

print()
print("🎯 CATEGORY-BASED TOPICS:")
print("-" * 40)

categories = {
    "Technology": ["AI news", "tech reviews", "software updates", "gadget trends"],
    "Health": ["fitness tips", "nutrition facts", "wellness guide", "medical news"],
    "Entertainment": ["movie reviews", "music trends", "celebrity news", "gaming updates"],
    "Education": ["learning resources", "study tips", "course reviews", "skill development"],
    "Travel": ["destination guides", "travel tips", "flight deals", "hotel reviews"],
    "Business": ["market news", "startup stories", "investment tips", "career advice"],
    "Lifestyle": ["fashion trends", "home decor", "cooking recipes", "life hacks"],
    "Sports": ["game highlights", "player stats", "team news", "sports analysis"]
}

for category, topics in categories.items():
    sample_topic = random.choice(topics)
    print(f"  {category}: {sample_topic}")

print()
print("✨ RANDOM COMBINATION EXAMPLES:")
print("-" * 40)

# Show random combinations
subjects = ["technology", "health", "travel", "food", "fitness"]
modifiers = ["latest", "best", "top", "new", "trending"]
types = ["news", "tips", "guide", "review", "facts"]

for i in range(5):
    combo = f"{random.choice(modifiers)} {random.choice(subjects)} {random.choice(types)}"
    print(f"  • {combo}")

print()
print("🔄 UNIQUENESS GUARANTEE:")
print("-" * 40)
print("Each run combines:")
print("  ✓ Current date & time")
print("  ✓ Random category selection") 
print("  ✓ Dynamic modifiers")
print("  ✓ Contextual keywords")
print("  ✓ Trending elements")
print()
print("Result: No two test runs will have identical topics!")
print("=" * 60)
"@

$ShowcasePath = Join-Path $ScriptDir "topic_showcase.py"
$ShowcaseCode | Out-File -FilePath $ShowcasePath -Encoding UTF8

Write-Host "Running topic variety showcase..." -ForegroundColor Green
& $PythonExe $ShowcasePath

Write-Host ""
Write-Host "🎯 QUICK START COMMANDS:" -ForegroundColor Cyan
Write-Host "  .\dynamic_test.ps1        - Test with unique topics (new browser)" -ForegroundColor White
Write-Host "  .\test_new_browser.ps1    - Standard test with dynamic topics" -ForegroundColor White
Write-Host "  .\quick_test.ps1          - Fast 3-search test with variety" -ForegroundColor White
Write-Host "  .\standalone_rewards.ps1  - Full rewards session with dynamic topics" -ForegroundColor White
Write-Host ""
Write-Host "Every script now uses different topics each time you run it! 🚀" -ForegroundColor Green