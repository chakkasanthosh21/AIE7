#!/usr/bin/env python3
"""
Script to open the Student Loan Assistant in Chrome browser
"""

import subprocess
import sys
import os
import time
import webbrowser
from urllib.parse import urlparse

def open_in_chrome():
    """Open the app in Chrome browser."""
    print("🎓 Student Loan Assistant - Chrome Launcher")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("app.py"):
        print("❌ Error: app.py not found. Please run this script from the certification_challenge directory.")
        sys.exit(1)
    
    # URL to open
    url = "http://localhost:8501"
    
    print(f"🌐 Opening {url} in Chrome...")
    print("⏳ Waiting for Streamlit to start...")
    
    # Wait a moment for Streamlit to start
    time.sleep(3)
    
    try:
        # Try to open in Chrome specifically
        chrome_path = None
        
        # Check for Chrome on different platforms
        if sys.platform == "darwin":  # macOS
            chrome_paths = [
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                "/Applications/Chromium.app/Contents/MacOS/Chromium"
            ]
        elif sys.platform.startswith("win"):  # Windows
            chrome_paths = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
            ]
        else:  # Linux
            chrome_paths = [
                "/usr/bin/google-chrome",
                "/usr/bin/chromium-browser",
                "/usr/bin/chromium"
            ]
        
        # Find Chrome
        for path in chrome_paths:
            if os.path.exists(path):
                chrome_path = path
                break
        
        if chrome_path:
            print(f"✅ Found Chrome at: {chrome_path}")
            # Open with specific Chrome path
            subprocess.Popen([chrome_path, url, "--new-window"])
        else:
            print("⚠️ Chrome not found in standard locations, using default browser...")
            # Use default browser (might be Chrome)
            webbrowser.open(url)
        
        print("✅ App should now be opening in Chrome!")
        print("\n💡 Tips:")
        print("   - If the page doesn't load, wait a few more seconds and refresh")
        print("   - Use the sidebar for quick actions and example queries")
        print("   - Try asking questions about student loans")
        print("   - Check the Evaluation tab for system performance")
        
    except Exception as e:
        print(f"❌ Error opening Chrome: {str(e)}")
        print("🔗 Please manually open Chrome and navigate to: http://localhost:8501")

def check_streamlit_running():
    """Check if Streamlit is running."""
    try:
        import requests
        response = requests.get("http://localhost:8501", timeout=5)
        return response.status_code == 200
    except:
        return False

if __name__ == "__main__":
    # Check if Streamlit is already running
    if check_streamlit_running():
        print("✅ Streamlit is already running!")
    else:
        print("⚠️ Streamlit doesn't seem to be running yet.")
        print("💡 Make sure to start Streamlit first with: streamlit run app.py")
        print("   Or use: python run_ui.py")
    
    open_in_chrome() 