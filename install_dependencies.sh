#!/bin/bash

# AIE7 Repository Dependencies Installation Script
# This script installs all necessary Python packages for the AIE7 repository

echo "🚀 Installing AIE7 repository dependencies..."

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if pip is available
if ! command -v pip &> /dev/null; then
    echo "❌ pip is not installed. Please install pip first."
    exit 1
fi

echo "📦 Installing core dependencies..."

# Install all dependencies from requirements.txt
pip install -r requirements.txt

echo "✅ Installation completed successfully!"
echo ""
echo "📋 Summary of installed packages:"
echo "   • Jupyter and notebook support"
echo "   • Data science libraries (pandas, numpy, matplotlib, plotly)"
echo "   • Machine learning libraries (scikit-learn, scipy)"
echo "   • OpenAI and AI libraries"
echo "   • Fine-tuning libraries (torch, transformers, accelerate, etc.)"
echo ""
echo "🎉 You're ready to start working with the AIE7 repository!"
echo ""
echo "💡 Next steps:"
echo "   1. Set up your OpenAI API key (see 00_OpenAI API Key Setup/)"
echo "   2. Start with the onramp tutorials in 00_Onramp/"
echo "   3. Explore the embeddings and RAG section in 02_Embeddings_and_RAG/" 