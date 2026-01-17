#!/usr/bin/env python3
"""
Launcher script for Student Loan Assistant UI
"""

import subprocess
import sys
import os

def main():
    """Launch the Streamlit UI."""
    print("🎓 Student Loan Assistant - UI Launcher")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("app.py"):
        print("❌ Error: app.py not found. Please run this script from the certification_challenge directory.")
        sys.exit(1)
    
    # Check if requirements are installed
    try:
        import streamlit
        import plotly
        print("✅ Dependencies found")
    except ImportError:
        print("📦 Installing dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    print("🚀 Starting Student Loan Assistant UI...")
    print("📱 The UI will open in your default web browser")
    print("🔗 URL: http://localhost:8501")
    print("\n💡 Tips:")
    print("   - Use the sidebar for quick actions")
    print("   - Try the example queries to get started")
    print("   - Check the Evaluation tab for system performance")
    print("   - Use Ctrl+C to stop the server")
    print("\n" + "=" * 50)
    
    # Launch Streamlit
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 UI stopped. Goodbye!")

if __name__ == "__main__":
    main() 