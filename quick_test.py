import sys
import os
sys.path.append(r'C:\Users\himan\Desktop\edge search')

# Import the main functions
from search_trending_edge import run_search_sequence

# Test with only 3 topics for human-like behavior testing
test_topics = [
    "weather today",
    "latest technology news", 
    "best restaurants near me"
]

print("Starting human-like behavior test with 3 searches...")
print("This test will demonstrate:")
print("- Human-like typing with realistic delays")
print("- Mouse movements and clicks")  
print("- Reading simulation with natural scrolling")
print("- Realistic pauses between actions")
print()
try:
    run_search_sequence(test_topics, headless=False, min_wait=10, max_wait=15, use_existing=True)
    print("Human-like behavior test completed successfully!")
except Exception as e:
    print(f"Test failed: {e}")
