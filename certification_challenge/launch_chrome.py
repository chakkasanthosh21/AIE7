#!/usr/bin/env python3
"""
Complete launcher for Student Loan Assistant in Chrome
Starts Streamlit and opens Chrome browser automatically
"""

import subprocess
import sys
import os
import time
import threading
import webbrowser
from urllib.parse import urlparse

def start_streamlit():
    """Start the Streamlit server."""
    print("🚀 Starting Streamlit server...")
    
    try:
        # Start Streamlit in the background
        process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print("✅ Streamlit server started!")
        return process
    except Exception as e:
        print(f"❌ Error starting Streamlit: {str(e)}")
        return None

def wait_for_server():
    """Wait for the server to be ready."""
    print("⏳ Waiting for server to be ready...")
    
    for i in range(30):  # Wait up to 30 seconds
        try:
            import requests
            response = requests.get("http://localhost:8501", timeout=2)
            if response.status_code == 200:
                print("✅ Server is ready!")
                return True
        except:
            pass
        
        time.sleep(1)
        if i % 5 == 0:
            print(f"   Still waiting... ({i+1}/30 seconds)")
    
    print("⚠️ Server might not be ready yet, but trying to open browser anyway...")
    return False

def open_chrome():
    """Open Chrome browser to the app."""
    url = "http://localhost:8501"
    
    print(f"🌐 Opening Chrome to {url}...")
    
    try:
        # Try to find Chrome on macOS
        chrome_paths = [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Chromium.app/Contents/MacOS/Chromium"
        ]
        
        chrome_found = False
        for path in chrome_paths:
            if os.path.exists(path):
                print(f"✅ Found Chrome at: {path}")
                subprocess.Popen([path, url, "--new-window"])
                chrome_found = True
                break
        
        if not chrome_found:
            print("⚠️ Chrome not found, using default browser...")
            webbrowser.open(url)
        
        print("✅ Browser should be opening now!")
        
    except Exception as e:
        print(f"❌ Error opening browser: {str(e)}")
        print(f"🔗 Please manually open Chrome and go to: {url}")

def main():
    """Main launcher function."""
    print("🎓 Student Loan Assistant - Chrome Launcher")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("app.py"):
        print("❌ Error: app.py not found. Please run this script from the certification_challenge directory.")
        sys.exit(1)
    
    # Check if dependencies are installed
    try:
        import streamlit
        print("✅ Streamlit found")
    except ImportError:
        print("📦 Installing dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Start Streamlit
    streamlit_process = start_streamlit()
    if not streamlit_process:
        sys.exit(1)
    
    # Wait for server to be ready
    if wait_for_server():
        print("🎉 Server is ready!")
    else:
        print("⚠️ Server might still be starting...")
    
    # Open Chrome
    open_chrome()
    
    print("\n" + "=" * 50)
    print("🎯 Your Student Loan Assistant is now running!")
    print("\n💡 Tips:")
    print("   - The app is running at: http://localhost:8501")
    print("   - Use the sidebar for quick actions and example queries")
    print("   - Try asking questions about student loans")
    print("   - Check the Evaluation tab for system performance")
    print("   - Use Ctrl+C in this terminal to stop the server")
    print("\n🚀 Happy learning about student loans!")
    
    try:
        # Keep the script running
        streamlit_process.wait()
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
        streamlit_process.terminate()
        print("✅ Server stopped. Goodbye!")

if __name__ == "__main__":
    main() 