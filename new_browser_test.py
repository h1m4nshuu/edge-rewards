import sys
import os
sys.path.append(r'C:\Users\himan\Desktop\edge search')

# Import the main functions
from search_trending_edge import run_search_sequence

# Test with only 3 topics in NEW browser
test_topics = [
    "weather today",
    "latest news", 
    "technology updates"
]

print("Starting test with NEW browser window (3 searches)...")
print("This will not interfere with your regular Edge browsing.")
print()

try:
    # use_existing=False means it opens a NEW browser window
    run_search_sequence(test_topics, headless=False, min_wait=8, max_wait=12, use_existing=False)
    print()
    print("âœ… NEW browser test completed successfully!")
    print("The automation browser will close automatically.")
except Exception as e:
    print(f"âŒ Test failed: {e}")
