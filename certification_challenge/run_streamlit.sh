#!/bin/bash

# Student Loan Assistant - Streamlit Runner
echo "🎓 Student Loan Assistant - Streamlit Runner"
echo "=============================================="

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: app.py not found. Please run this script from the certification_challenge directory."
    exit 1
fi

# Set the Streamlit path
STREAMLIT_PATH="/Users/santhoshchaka/Library/Python/3.10/bin/streamlit"

# Check if Streamlit exists
if [ ! -f "$STREAMLIT_PATH" ]; then
    echo "❌ Error: Streamlit not found at $STREAMLIT_PATH"
    echo "💡 Try running: pip install streamlit"
    exit 1
fi

echo "✅ Found Streamlit at: $STREAMLIT_PATH"
echo "🚀 Starting Student Loan Assistant..."
echo "🌐 The app will open at: http://localhost:8501"
echo ""

# Run Streamlit
$STREAMLIT_PATH run app.py \
    --server.port 8501 \
    --server.address localhost \
    --browser.gatherUsageStats false \
    --server.headless false 