"""
Simple test script to check EdgeDriver compatibility
"""

from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService

def test_edge_connection():
    print("Testing EdgeDriver compatibility...")
    
    # Try with minimal options first
    options = EdgeOptions()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    try:
        print("Attempting to connect to existing Edge browser...")
        driver = webdriver.Edge(options=options)
        print("✓ Successfully connected to Edge!")
        
        # Test basic functionality
        driver.get("https://www.bing.com")
        print("✓ Successfully navigated to Bing!")
        
        # Get page title
        title = driver.title
        print(f"✓ Page title: {title}")
        
        driver.quit()
        print("✓ Test completed successfully!")
        return True
        
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        return False

if __name__ == "__main__":
    test_edge_connection()