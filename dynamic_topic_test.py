import sys
import os
import random
import datetime
sys.path.append(r'C:\Users\himan\Desktop\edge search')

from search_trending_edge import run_search_sequence, generate_dynamic_topics

def create_unique_session_topics():
    """Create topics that are unique to this specific test session"""
    current_time = datetime.datetime.now()
    
    # Time-based uniqueness
    minute = current_time.minute
    hour = current_time.hour
    day = current_time.day
    
    unique_topics = []
    
    # Add timestamp-based topics
    unique_topics.extend([
        f"breaking news hour {hour}",
        f"weather update minute {minute}",
        f"trending now day {day}",
        f"latest updates {current_time.strftime('%H:%M')}"
    ])
    
    # Random combinations for maximum variety
    subjects = ["technology", "science", "health", "entertainment", "sports", "business", "travel", "education"]
    actions = ["news", "updates", "trends", "facts", "tips", "guide", "review", "analysis"]
    timeframes = ["today", "2024", "latest", "recent", "current", "new", "fresh", "live"]
    
    # Generate random combinations
    for _ in range(15):
        subject = random.choice(subjects)
        action = random.choice(actions)
        time = random.choice(timeframes)
        
        # Different combination patterns
        patterns = [
            f"{time} {subject} {action}",
            f"{subject} {action} {time}",
            f"best {subject} {action}",
            f"{action} about {subject}",
            f"top {subject} {time}"
        ]
        
        topic = random.choice(patterns)
        if topic not in unique_topics:
            unique_topics.append(topic)
    
    return unique_topics

def show_topic_variety():
    """Show how topics change each run"""
    print("ðŸŽ² TOPIC VARIETY DEMONSTRATION:")
    print("=" * 50)
    
    for i in range(3):
        topics = generate_dynamic_topics(5)
        print(f"Run {i+1}: {topics}")
    
    print("=" * 50)
    print("As you can see, topics are different every time!")
    print()

# Show the variety
show_topic_variety()

# Generate unique topics for this session
session_topics = create_unique_session_topics()
test_topics = random.sample(session_topics, 3)

print("ðŸš€ STARTING UNIQUE TEST SESSION")
print(f"ðŸ“… Session Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"ðŸŽ¯ Today's Unique Topics: {test_topics}")
print()
print("This test uses completely different topics every time you run it!")
print("Opening NEW browser window for testing...")
print()

try:
    # Use NEW browser with unique topics
    run_search_sequence(test_topics, headless=False, min_wait=6, max_wait=10, use_existing=False)
    print()
    print("âœ… UNIQUE TOPIC TEST COMPLETED!")
    print("ðŸ”„ Run again to see completely different topics!")
except Exception as e:
    print(f"âŒ Test failed: {e}")
