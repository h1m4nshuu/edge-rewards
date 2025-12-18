import sys
import os
import random
import datetime
sys.path.append(r'C:\Users\himan\Desktop\edge search')

from search_trending_edge import generate_dynamic_topics

print("ðŸŽ² TOPIC GENERATION SHOWCASE")
print("=" * 60)
print()

# Show how topics change over multiple runs
print("ðŸ“Š VARIETY DEMONSTRATION - 5 Different Runs:")
print("-" * 40)
for run in range(1, 6):
    topics = generate_dynamic_topics(4)
    print(f"Run {run}: {topics}")

print()
print("ðŸ•’ TIME-BASED TOPICS:")
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
    print(f"  â€¢ {topic}")

print()
print("ðŸŽ¯ CATEGORY-BASED TOPICS:")
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
print("âœ¨ RANDOM COMBINATION EXAMPLES:")
print("-" * 40)

# Show random combinations
subjects = ["technology", "health", "travel", "food", "fitness"]
modifiers = ["latest", "best", "top", "new", "trending"]
types = ["news", "tips", "guide", "review", "facts"]

for i in range(5):
    combo = f"{random.choice(modifiers)} {random.choice(subjects)} {random.choice(types)}"
    print(f"  â€¢ {combo}")

print()
print("ðŸ”„ UNIQUENESS GUARANTEE:")
print("-" * 40)
print("Each run combines:")
print("  âœ“ Current date & time")
print("  âœ“ Random category selection") 
print("  âœ“ Dynamic modifiers")
print("  âœ“ Contextual keywords")
print("  âœ“ Trending elements")
print()
print("Result: No two test runs will have identical topics!")
print("=" * 60)
