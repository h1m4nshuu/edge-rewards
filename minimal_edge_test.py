"""
Ultra-simple Edge automation test - minimal options
"""

from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions

def simple_edge_test():
    print("Testing minimal Edge connection...")
    
    # Absolutely minimal options
    options = EdgeOptions()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    try:
        # Try with no service specified (use system EdgeDriver)
        driver = webdriver.Edge(options=options)
        print("✓ Connected to Edge!")
        
        driver.get("https://www.bing.com")
        print(f"✓ Page title: {driver.title}")
        
        driver.quit()
        return True
        
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False

if __name__ == "__main__":
    if simple_edge_test():
        print("SUCCESS: Edge connection works!")
        exit(0)
    else:
        print("FAILED: Could not connect to Edge")
        exit(1)