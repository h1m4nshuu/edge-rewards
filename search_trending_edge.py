"""
search_trending_edge.py

Edge (Chromium) + Selenium script that:
- chooses 30 trending topics (via pytrends if available, otherwise fallback list),
- opens each topic in Microsoft Edge,
- scrolls the page in human-like steps,
- waits a random interval between 50 and 55 seconds between searches.

Requirements:
  pip install selenium webdriver-manager pytrends
  Microsoft Edge (Chromium) installed on the machine.
"""

import time
import random
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Edge-specific imports
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# Optional: pytrends to fetch trending searches
try:
    from pytrends.request import TrendReq
    HAVE_PYTRENDS = True
except Exception:
    HAVE_PYTRENDS = False

def fetch_trending_queries(limit=100, region='global'):
    """
    Tries to fetch trending search queries via pytrends.
    If pytrends is not available or fetching fails, returns None.
    """
    if not HAVE_PYTRENDS:
        return None
    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        if region.lower() in ['global', 'world', 'globe']:
            df = pytrends.trending_searches(pn='global')
        else:
            df = pytrends.trending_searches(pn=region)
        queries = [str(x) for x in df[0].tolist()]
        return queries[:limit]
    except Exception:
        return None

# Expanded topic pools for variety
BASE_TOPICS = [
    "AI image generator", "World Cup", "Bitcoin price", "Stock market today",
    "Weather near me", "SpaceX launch", "New movie release", "Elon Musk",
    "ChatGPT", "Taylor Swift", "Oscars 2025", "Climate change news",
    "Olympics updates", "Tech layoffs", "Electric vehicles", "Quantum computing",
    "Mars rover", "Best programming languages 2025", "Python tutorial",
    "How to learn machine learning", "Healthy recipes", "Meditation benefits",
    "Top colleges 2025", "Study tips", "Internship opportunities", "Scholarship 2025",
    "Remote jobs", "Productivity hacks", "Fitness at home", "Budget travel tips",
    "Smartphone reviews", "Cybersecurity threats", "Cloud computing trends"
]

TOPIC_CATEGORIES = {
    "technology": ["artificial intelligence", "machine learning", "blockchain", "5G network", "virtual reality", 
                   "augmented reality", "IoT devices", "cloud computing", "cybersecurity", "quantum computing",
                   "robotics", "smart home", "autonomous cars", "drone technology", "3D printing"],
    
    "news_current": ["breaking news", "world news", "political updates", "economic forecast", "social media trends",
                     "viral videos", "celebrity gossip", "sports highlights", "weather alerts", "stock market"],
    
    "lifestyle": ["healthy recipes", "fitness workout", "yoga poses", "meditation guide", "home decor",
                  "fashion trends", "beauty tips", "skincare routine", "hair care", "makeup tutorial"],
    
    "education": ["online courses", "study tips", "language learning", "programming tutorial", "math help",
                  "science facts", "history timeline", "geography quiz", "literature review", "exam preparation"],
    
    "entertainment": ["movie reviews", "TV shows", "music playlist", "podcast recommendations", "book reviews",
                      "gaming news", "streaming services", "concert tickets", "theater shows", "art exhibitions"],
    
    "travel": ["travel destinations", "flight deals", "hotel booking", "travel tips", "local cuisine",
               "tourist attractions", "travel insurance", "packing tips", "budget travel", "adventure sports"],
    
    "shopping": ["product reviews", "best deals", "shopping guide", "price comparison", "gift ideas",
                 "online shopping", "discount codes", "product recommendations", "brand comparison", "sales alerts"],
    
    "health": ["medical advice", "nutrition facts", "mental health", "exercise benefits", "sleep tips",
               "vitamin supplements", "disease prevention", "health insurance", "doctor consultation", "wellness tips"]
}

MODIFIERS = [
    "2024", "2025", "latest", "best", "top", "new", "trending", "popular", "guide", "tips",
    "review", "comparison", "how to", "benefits of", "facts about", "news", "updates", 
    "today", "this week", "explained", "tutorial", "beginner", "advanced", "free", "cheap"
]

def generate_dynamic_topics(count=30):
    """
    Generates dynamic, varied search topics that are different each time.
    """
    import datetime
    
    topics = []
    used_topics = set()
    
    # Add some time-based topics for uniqueness
    current_time = datetime.datetime.now()
    time_based_topics = [
        f"news {current_time.strftime('%B %Y')}",
        f"weather {current_time.strftime('%A')}",
        f"events {current_time.strftime('%B %d')}",
        f"trending {current_time.strftime('%Y')}",
        f"updates {current_time.strftime('%B')}"
    ]
    
    # Add time-based topics first
    for topic in time_based_topics[:5]:
        if topic not in used_topics:
            topics.append(topic)
            used_topics.add(topic)
    
    # Generate topics from categories
    categories = list(TOPIC_CATEGORIES.keys())
    random.shuffle(categories)
    
    for category in categories:
        if len(topics) >= count:
            break
            
        category_topics = TOPIC_CATEGORIES[category].copy()
        random.shuffle(category_topics)
        
        # Take 3-5 topics from each category
        for topic in category_topics[:random.randint(3, 5)]:
            if len(topics) >= count:
                break
                
            # Sometimes add modifiers for variety
            if random.random() < 0.6:  # 60% chance
                modifier = random.choice(MODIFIERS)
                if random.choice([True, False]):
                    enhanced_topic = f"{modifier} {topic}"
                else:
                    enhanced_topic = f"{topic} {modifier}"
            else:
                enhanced_topic = topic
            
            if enhanced_topic not in used_topics:
                topics.append(enhanced_topic)
                used_topics.add(enhanced_topic)
    
    # Fill remaining slots with base topics if needed
    remaining_base = BASE_TOPICS.copy()
    random.shuffle(remaining_base)
    
    for topic in remaining_base:
        if len(topics) >= count:
            break
            
        if topic not in used_topics:
            # Add variation to base topics too
            if random.random() < 0.4:  # 40% chance
                modifier = random.choice(MODIFIERS)
                enhanced_topic = f"{topic} {modifier}"
            else:
                enhanced_topic = topic
                
            if enhanced_topic not in used_topics:
                topics.append(enhanced_topic)
                used_topics.add(enhanced_topic)
    
    # Shuffle the final list
    random.shuffle(topics)
    return topics[:count]

# Keep original for backward compatibility
SAMPLE_TOPICS = generate_dynamic_topics(50)  # Generate 50 topics to choose from

def human_type(element, text, min_delay=0.05, max_delay=0.25):
    """
    Types text character by character with human-like delays and occasional mistakes.
    """
    actions = ActionChains(element.parent)
    
    # Clear the field first with realistic selection
    element.click()
    time.sleep(random.uniform(0.1, 0.3))
    actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
    time.sleep(random.uniform(0.05, 0.15))
    
    # Type character by character
    for i, char in enumerate(text):
        # Random typing speed variation
        if char == ' ':
            delay = random.uniform(0.1, 0.3)  # Longer pause at spaces
        elif char in '.,!?':
            delay = random.uniform(0.2, 0.4)  # Pause at punctuation
        else:
            delay = random.uniform(min_delay, max_delay)
        
        # Occasional typo simulation (5% chance)
        if random.random() < 0.05 and i > 2:
            # Type wrong character, pause, then backspace and correct
            wrong_chars = 'qwertyuiopasdfghjklzxcvbnm'
            wrong_char = random.choice(wrong_chars)
            element.send_keys(wrong_char)
            time.sleep(random.uniform(0.1, 0.3))
            element.send_keys(Keys.BACKSPACE)
            time.sleep(random.uniform(0.05, 0.2))
        
        element.send_keys(char)
        time.sleep(delay)
        
        # Occasional hesitation (10% chance)
        if random.random() < 0.1:
            time.sleep(random.uniform(0.3, 0.8))

def human_mouse_movement(driver, element):
    """
    Moves mouse to element in a human-like curved path.
    """
    actions = ActionChains(driver)
    
    # Get current window size for realistic movement
    window_size = driver.get_window_size()
    
    # Simulate moving mouse from random starting position
    start_x = random.randint(100, window_size['width'] - 100)
    start_y = random.randint(100, window_size['height'] - 100)
    
    # Get element location
    element_location = element.location
    element_size = element.size
    target_x = element_location['x'] + element_size['width'] // 2
    target_y = element_location['y'] + element_size['height'] // 2
    
    # Create curved movement path
    steps = random.randint(8, 15)
    for step in range(steps):
        progress = step / steps
        
        # Add some curve and randomness
        curve_offset_x = random.randint(-20, 20) * (1 - progress)
        curve_offset_y = random.randint(-15, 15) * (1 - progress)
        
        current_x = start_x + (target_x - start_x) * progress + curve_offset_x
        current_y = start_y + (target_y - start_y) * progress + curve_offset_y
        
        # Small random delay between movements
        time.sleep(random.uniform(0.01, 0.03))
    
    # Final move to exact element
    actions.move_to_element(element).perform()
    time.sleep(random.uniform(0.1, 0.3))

def human_click(driver, element):
    """
    Performs a human-like click with mouse movement and realistic timing.
    """
    # Move mouse to element first
    human_mouse_movement(driver, element)
    
    # Brief pause before clicking (like humans do)
    time.sleep(random.uniform(0.1, 0.4))
    
    # Click with slight randomness in timing
    actions = ActionChains(driver)
    actions.click(element).perform()
    
    # Brief pause after click
    time.sleep(random.uniform(0.1, 0.3))

def simulate_reading_behavior(driver):
    """
    Simulates human reading behavior - random scrolls, pauses, etc.
    """
    # Random small scrolls as if reading
    for _ in range(random.randint(2, 5)):
        scroll_amount = random.randint(50, 200)
        driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
        time.sleep(random.uniform(0.8, 2.5))  # Reading time
        
        # Occasional scroll back up (like re-reading)
        if random.random() < 0.3:
            back_scroll = random.randint(20, 100)
            driver.execute_script(f"window.scrollBy(0, -{back_scroll});")
            time.sleep(random.uniform(0.5, 1.2))
    
    # Sometimes scroll to bottom of visible area
    if random.random() < 0.4:
        driver.execute_script("window.scrollBy(0, window.innerHeight * 0.8);")
        time.sleep(random.uniform(1.0, 2.0))

def random_human_pause():
    """
    Adds realistic human pauses between actions.
    """
    pause_type = random.choice(['short', 'medium', 'long', 'thinking'])
    
    if pause_type == 'short':
        time.sleep(random.uniform(0.3, 0.8))
    elif pause_type == 'medium':
        time.sleep(random.uniform(0.8, 1.5))
    elif pause_type == 'long':
        time.sleep(random.uniform(1.5, 3.0))
    elif pause_type == 'thinking':
        time.sleep(random.uniform(2.0, 4.0))

def perform_rewards_qualifying_actions(driver, search_term):
    """
    Performs specific actions that help qualify searches for Microsoft Rewards.
    """
    try:
        # Check for Bing rewards-related elements
        rewards_elements = driver.find_elements(By.CSS_SELECTOR, 
            ".rewards, .rewardsbadge, .ms-rewards, [data-testid*='reward'], .earnpoints")
        
        if rewards_elements:
            print("  -> Microsoft Rewards elements detected")
        
        # Look for and interact with different search result types
        # Images tab (sometimes helps with variety)
        if random.random() < 0.2:  # 20% chance
            try:
                images_tab = driver.find_element(By.CSS_SELECTOR, "a[href*='images']")
                if images_tab:
                    print("  -> Checking images results...")
                    human_click(driver, images_tab)
                    time.sleep(random.uniform(2, 4))
                    # Go back to web results
                    web_tab = driver.find_element(By.CSS_SELECTOR, "a[href*='search'][href*='q=']")
                    if web_tab:
                        human_click(driver, web_tab)
                        time.sleep(random.uniform(1, 2))
            except Exception:
                pass
        
        # Look for news results (another variety signal)
        if random.random() < 0.2:  # 20% chance
            try:
                news_tab = driver.find_element(By.CSS_SELECTOR, "a[href*='news']")
                if news_tab:
                    print("  -> Checking news results...")
                    human_click(driver, news_tab)
                    time.sleep(random.uniform(2, 4))
                    # Go back to web results
                    web_tab = driver.find_element(By.CSS_SELECTOR, "a[href*='search'][href*='q=']")
                    if web_tab:
                        human_click(driver, web_tab)
                        time.sleep(random.uniform(1, 2))
            except Exception:
                pass
        
        # Interact with search suggestions or related searches
        try:
            related_searches = driver.find_elements(By.CSS_SELECTOR, 
                ".b_rs, .related-search, .suggestion, [data-testid*='suggestion']")
            if related_searches and random.random() < 0.1:  # 10% chance
                suggestion = random.choice(related_searches[:3])
                print("  -> Checking related search suggestion...")
                human_mouse_movement(driver, suggestion)
                time.sleep(random.uniform(0.5, 1.0))
        except Exception:
            pass
            
    except Exception as e:
        print(f"  -> Could not perform rewards actions: {e}")

def click_search_result(driver):
    """
    Occasionally clicks on search results to show genuine engagement.
    """
    try:
        # Find search result links (but avoid ads)
        result_links = driver.find_elements(By.CSS_SELECTOR, 
            "h2 a, .b_title a, .b_algo h2 a, [data-testid='result'] a")
        
        # Filter out ad results and keep only organic results
        organic_results = []
        for link in result_links[:8]:  # Only check first 8 results
            try:
                href = link.get_attribute('href')
                # Skip ads, Microsoft sites, and suspicious links
                if (href and 
                    'bing.com/aclick' not in href and 
                    'msn.com/aclick' not in href and
                    len(href) > 20):
                    organic_results.append(link)
            except Exception:
                continue
        
        if organic_results:
            # Click on a random organic result
            result_to_click = random.choice(organic_results[:5])  # Top 5 results only
            print("  -> Clicking on search result for deeper engagement...")
            
            # Scroll to result first
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", result_to_click)
            time.sleep(random.uniform(1, 2))
            
            # Human-like click
            human_click(driver, result_to_click)
            
            # Stay on the page briefly (like reading)
            time.sleep(random.uniform(3, 8))
            
            # Sometimes scroll on the destination page
            if random.random() < 0.7:  # 70% chance
                scroll_amount = random.randint(200, 600)
                driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
                time.sleep(random.uniform(2, 4))
            
            # Go back to search results
            driver.back()
            time.sleep(random.uniform(2, 4))
            print("  -> Returned to search results")
            
    except Exception as e:
        print(f"  -> Could not click search result: {e}")

def build_edge_driver(headless=False, window_size=(1200, 800), use_existing=False, debug_port=9222):
    options = EdgeOptions()
    
    if use_existing:
        # Connect to existing Edge browser - use minimal options for maximum compatibility
        print(f"Connecting to existing Edge browser on port {debug_port}...")
        options.add_experimental_option("debuggerAddress", f"127.0.0.1:{debug_port}")
    else:
        # New browser instance with human-like settings
        if headless:
            options.add_argument("--headless=new")
        
        # Randomize window size to look more human
        width = random.randint(1200, 1600)
        height = random.randint(800, 1000)
        options.add_argument(f"--window-size={width},{height}")
        
        # Add human-like browser arguments
        options.add_argument("--disable-extensions")
        options.add_argument("--no-first-run")
        options.add_argument("--disable-default-apps")
        
        # Set realistic user agent and preferences
        options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Add realistic preferences
        prefs = {
            "profile.default_content_setting_values": {
                "notifications": 2,  # Block notifications
                "geolocation": 2     # Block location requests
            },
            "profile.managed_default_content_settings": {
                "images": 1  # Allow images
            }
        }
        options.add_experimental_option("prefs", prefs)

    # Try to get Edge driver with better error handling
    driver = None
    
    # First try system EdgeDriver (more reliable for existing browser connections)
    try:
        print("Trying to use system-installed EdgeDriver...")
        driver = webdriver.Edge(options=options)
        print("Successfully connected using system EdgeDriver!")
    except Exception as e1:
        print(f"System EdgeDriver failed: {e1}")
        
        # If that fails, try auto-download (but skip if connecting to existing browser)
        if not use_existing:
            try:
                print("Trying to auto-download EdgeDriver...")
                service = EdgeService(EdgeChromiumDriverManager().install())
                driver = webdriver.Edge(service=service, options=options)
                print("Successfully connected using downloaded EdgeDriver!")
            except Exception as e2:
                print(f"Auto-download EdgeDriver failed: {e2}")
        
        if driver is None:
            print(f"All EdgeDriver methods failed.")
            if use_existing:
                print("\nTo use existing Edge browser:")
                print("1. Make sure Edge is running with: msedge.exe --remote-debugging-port=9222")
                print("2. Ensure EdgeDriver is in your system PATH")
                print("3. Download EdgeDriver from: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/")
            else:
                print("Please ensure Microsoft Edge WebDriver is installed or available in PATH.")
                print("You can download it from: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/")
            raise Exception("Could not initialize EdgeDriver")

    # Make browser appear more human-like
    try:
        if not use_existing:  # Only try this for new browser instances
            # Override automation detection
            driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
                    Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                    Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
                    Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
                    window.chrome = {runtime: {}};
                """
            })
            
            # Set realistic viewport
            width = random.randint(1200, 1600)
            height = random.randint(800, 1000)
            driver.execute_cdp_cmd("Emulation.setDeviceMetricsOverride", {
                "width": width,
                "height": height,
                "deviceScaleFactor": 1,
                "mobile": False
            })
            
    except Exception:
        # Some environments may not support CDP calls; continue without it.
        pass
    
    # Set random position on screen (like a human opening browser)
    if not use_existing and not headless:
        try:
            x = random.randint(50, 200)
            y = random.randint(50, 150)
            driver.set_window_position(x, y)
        except Exception:
            pass

    return driver

def human_scroll(driver, min_steps=4, max_steps=8, min_pause=0.6, max_pause=1.6):
    """
    Scroll in several randomized steps to simulate human reading/scrolling.
    """
    try:
        page_height = driver.execute_script("return document.body.scrollHeight")
        steps = random.randint(min_steps, max_steps)
        scroll_so_far = 0
        for _ in range(steps):
            remaining = page_height - scroll_so_far
            if remaining <= 0:
                break
            fraction = random.uniform(0.12, 0.35)
            move = int(page_height * fraction)
            scroll_so_far += move
            if scroll_so_far > page_height:
                scroll_so_far = page_height
            driver.execute_script(f"window.scrollTo(0, {scroll_so_far});")
            time.sleep(random.uniform(min_pause, max_pause))

        # small back-and-forth movement occasionally
        if random.random() < 0.4:
            driver.execute_script("window.scrollBy(0, -120);")
            time.sleep(random.uniform(0.3, 0.9))
            driver.execute_script("window.scrollBy(0, 80);")
    except Exception:
        # Fallback: page-down key presses
        for _ in range(random.randint(2, 6)):
            try:
                ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
                time.sleep(random.uniform(0.5, 1.0))
            except Exception:
                break

def ensure_microsoft_account_login(driver):
    """
    Checks if user is logged into Microsoft account for rewards.
    """
    try:
        # Check if already logged in by looking for profile/account elements
        profile_elements = driver.find_elements(By.CSS_SELECTOR, "[data-testid='profile-button'], .id_button, .profile, [aria-label*='Account'], .me-control")
        if profile_elements:
            print("  -> Microsoft account detected - rewards should be active")
            return True
        else:
            print("  -> No Microsoft account detected")
            print("  -> Please manually sign into your Microsoft account in this browser")
            print("  -> Then restart the automation for reward points to count")
            return False
    except Exception:
        print("  -> Could not verify Microsoft account status")
        return False

def ensure_rewards_eligible_behavior(driver):
    """
    Performs additional actions to ensure searches qualify for Microsoft Rewards.
    """
    try:
        # Check for and interact with Bing homepage elements (shows engagement)
        time.sleep(random.uniform(2, 4))
        
        # Look for news, images, or other Bing features to interact with
        interactive_elements = driver.find_elements(By.CSS_SELECTOR, 
            ".hp_sw_logo, .hp_sw, .b_searchbox, .news, .trending, .hp_bottom")
        
        if interactive_elements:
            # Occasionally interact with homepage elements (like a curious user)
            if random.random() < 0.3:  # 30% chance
                element = random.choice(interactive_elements[:3])  # Only first 3 to be safe
                try:
                    human_mouse_movement(driver, element)
                    time.sleep(random.uniform(0.5, 1.0))
                    print("  -> Engaging with Bing homepage content...")
                except Exception:
                    pass
        
        # Scroll slightly on homepage (shows engagement)
        if random.random() < 0.5:  # 50% chance
            scroll_amount = random.randint(100, 300)
            driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            time.sleep(random.uniform(1, 2))
            driver.execute_script("window.scrollTo(0, 0);")  # Back to top
            
    except Exception as e:
        print(f"  -> Could not perform engagement actions: {e}")

def run_search_sequence(topics, headless=False, min_wait=50, max_wait=55, use_existing=False):
    driver = build_edge_driver(headless=headless, use_existing=use_existing)
    try:
        # Navigate to Bing and check for Microsoft account
        print("Initializing Bing and checking Microsoft Rewards eligibility...")
        driver.get("https://www.bing.com")
        time.sleep(random.uniform(3, 5))  # Extra time for page load
        
        # Check Microsoft account status
        is_logged_in = ensure_microsoft_account_login(driver)
        
        # Attempt to close common consent dialogs (best-effort)
        try:
            buttons = driver.find_elements(By.TAG_NAME, "button")
            for b in buttons[:12]:
                txt = (b.text or "").lower()
                if any(k in txt for k in ["accept", "agree", "i agree", "all", "consent", "yes", "allow"]):
                    try:
                        human_click(driver, b)
                        time.sleep(2.0)
                        break
                    except Exception:
                        pass
        except Exception:
            pass
        
        # Perform pre-search engagement
        ensure_rewards_eligible_behavior(driver)

        for idx, topic in enumerate(topics, 1):
            print(f"[{idx}/{len(topics)}] Searching: {topic}")
            try:
                # Check if browser is still connected
                try:
                    driver.current_url  # Test connection
                except Exception:
                    print(f"  -> Browser disconnected! Skipping remaining searches.")
                    print("  -> This happens when the browser window is closed manually.")
                    break
                
                # Navigate to search page like a human would
                if idx == 1:
                    # First search - go to Bing homepage first
                    print("  -> Navigating to Bing...")
                    driver.get("https://www.bing.com")
                    random_human_pause()
                else:
                    # Subsequent searches - use search box or go to new page
                    if random.choice([True, False]):
                        # Sometimes go to fresh Bing page
                        driver.get("https://www.bing.com")
                        random_human_pause()
                
                # Wait for page to load completely
                try:
                    wait = WebDriverWait(driver, 10)
                    search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))
                except Exception:
                    # Fallback to direct URL if search box not found
                    q = urllib.parse.quote_plus(topic)
                    search_url = f"https://www.bing.com/search?q={q}"
                    driver.get(search_url)
                    time.sleep(random.uniform(2.0, 4.0))
                    human_scroll(driver)
                    continue
                
                # Human-like interaction with search box
                print(f"  -> Typing search query...")
                
                # Click on search box with human-like mouse movement
                human_click(driver, search_box)
                random_human_pause()
                
                # Type the search query with human-like typing
                human_type(search_box, topic)
                
                # Random pause before pressing enter (like humans thinking)
                time.sleep(random.uniform(0.5, 1.5))
                
                # Press Enter to search
                search_box.send_keys(Keys.RETURN)
                
                # Wait for results to load completely
                time.sleep(random.uniform(3.0, 5.0))  # Longer wait for full page load
                
                # Verify page loaded and simulate human reading behavior
                try:
                    driver.title  # Test that page is accessible
                    print(f"  -> Engaging with search results...")
                    
                    # Enhanced result interaction for Microsoft Rewards
                    perform_rewards_qualifying_actions(driver, topic)
                    
                    # Simulate human reading and scrolling behavior
                    simulate_reading_behavior(driver)
                    
                    # Additional human-like scrolling
                    human_scroll(driver)
                    
                    # Sometimes click on search result links (major engagement signal)
                    if random.random() < 0.4:  # 40% chance
                        click_search_result(driver)
                    
                    print(f"  -> Successfully searched: {topic}")
                    
                except Exception as scroll_error:
                    print(f"  -> Could not interact with page for '{topic}': {scroll_error}")
                    
            except Exception as e:
                print(f"  -> Error searching '{topic}': {e}")
                # If it's a session error, break the loop
                if "invalid session id" in str(e) or "no such window" in str(e):
                    print("  -> Browser session lost. Stopping automation.")
                    break

            # Human-like wait time with some variation
            base_wait = random.uniform(min_wait, max_wait)
            # Add occasional longer pauses (like humans getting distracted)
            if random.random() < 0.1:  # 10% chance of longer pause
                extra_wait = random.uniform(10, 30)
                print(f"  -> Taking a longer break ({extra_wait:.1f}s additional)...")
                time.sleep(extra_wait)
            
            wait_time = base_wait
            print(f"  -> Waiting {wait_time:.1f}s before next search...")
            time.sleep(wait_time)

    finally:
        print("All searches finished. Closing browser.")
        driver.quit()

if __name__ == "__main__":
    import sys
    
    # Default settings (optimized for Microsoft Rewards)
    HEADLESS = False
    USE_EXISTING = False
    MIN_WAIT = 35  # Increased for better reward qualification
    MAX_WAIT = 50  # Increased for better reward qualification  
    TOPIC_COUNT = 30
    
    # Check for command line arguments
    if "--headless" in sys.argv:
        HEADLESS = True
        print("Running in headless mode.")
    
    if "--existing" in sys.argv:
        USE_EXISTING = True
        print("Attempting to use existing Edge browser.")
    
    if "--help" in sys.argv or "-h" in sys.argv:
        print("Usage: python search_trending_edge.py [--headless] [--existing] [--help]")
        print("  --headless    Run browser in headless mode (invisible)")
        print("  --existing    Connect to existing Edge browser (requires setup)")
        print("  --help, -h    Show this help message")
        print("\nTo use existing Edge browser:")
        print("1. Close all Edge windows")
        print("2. Open PowerShell and run: msedge.exe --remote-debugging-port=9222")
        print("3. Then run this script with --existing flag")
        sys.exit(0)

    print("Starting Edge search automation...")
    print(f"Configuration: Headless={HEADLESS}, Wait={MIN_WAIT}-{MAX_WAIT}s, Topics={TOPIC_COUNT}")
    
    # Try to fetch trending queries first
    queries = fetch_trending_queries(limit=200, region='global')
    
    if not queries:
        print("Couldn't fetch live trending queries; generating dynamic topics...")
        # Generate fresh, dynamic topics every time
        queries = generate_dynamic_topics(TOPIC_COUNT * 2)  # Generate more than needed for variety
    else:
        print(f"Using {len(queries)} trending queries from pytrends...")
        # Even with trending queries, add some generated ones for variety
        dynamic_topics = generate_dynamic_topics(TOPIC_COUNT // 2)
        queries.extend(dynamic_topics)

    # Ensure we have enough topics
    if len(queries) < TOPIC_COUNT:
        # Generate additional dynamic topics if needed
        additional_topics = generate_dynamic_topics(TOPIC_COUNT - len(queries) + 10)
        queries.extend(additional_topics)

    # Remove duplicates while preserving order
    unique_queries = []
    seen = set()
    for query in queries:
        query_lower = query.lower()
        if query_lower not in seen:
            unique_queries.append(query)
            seen.add(query_lower)
    
    queries = unique_queries

    # Select random topics from the pool
    chosen = random.sample(queries, min(TOPIC_COUNT, len(queries)))
    
    # Add some variation to make searches more unique (helps with rewards)
    unique_searches = []
    for topic in chosen:
        # Sometimes add variations to make searches more unique
        if random.random() < 0.3:  # 30% chance of variation
            variations = [
                f"{topic} 2024",
                f"{topic} news", 
                f"{topic} today",
                f"{topic} latest",
                f"best {topic}",
                f"{topic} guide",
                f"{topic} tips"
            ]
            topic = random.choice(variations)
        unique_searches.append(topic)
    
    print(f"\nStarting Microsoft Rewards-optimized search sequence...")
    print(f"Tips for maximum reward points:")
    print("- Make sure you're signed into your Microsoft account")
    print("- Don't close the browser window during searches") 
    print("- Let the automation complete all searches")
    print("- Searches include engagement actions for better reward qualification\n")
    
    try:
        run_search_sequence(unique_searches, headless=HEADLESS, min_wait=MIN_WAIT, max_wait=MAX_WAIT, use_existing=USE_EXISTING)
    except Exception as e:
        print(f"\nError running search sequence: {e}")
        if USE_EXISTING:
            print("If using --existing, make sure Edge is running with remote debugging enabled.")
        print("Please check that Microsoft Edge is installed and EdgeDriver is available.")
        sys.exit(1)
