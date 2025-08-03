#!/bin/bash

# Student Loan Assistant - Docker Runner
echo "🎓 Student Loan Assistant - Docker Runner"
echo "=============================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker is not installed. Please install Docker first."
    echo "💡 Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Error: Docker Compose is not installed. Please install Docker Compose first."
    echo "💡 Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found. Creating template..."
    cat > .env << EOF
# API Keys (Required)
OPENAI_API_KEY=your_openai_api_key_here
COHERE_API_KEY=your_cohere_api_key_here

# Optional: Customize these if needed
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
EOF
    echo "📝 Created .env template. Please edit it with your API keys."
    echo "💡 You can get API keys from:"
    echo "   - OpenAI: https://platform.openai.com/api-keys"
    echo "   - Cohere: https://dashboard.cohere.ai/api-keys"
    exit 1
fi

# Check if API keys are set
if grep -q "your_openai_api_key_here" .env; then
    echo "❌ Error: Please update your .env file with actual API keys."
    exit 1
fi

# Create necessary directories
mkdir -p data logs

# Copy data files if they exist in parent directory
if [ -d "../04_Production_RAG/data" ]; then
    echo "📁 Copying data files..."
    cp -r ../04_Production_RAG/data/* ./data/ 2>/dev/null || true
fi

echo "🐳 Building and starting Student Loan Assistant..."
echo "⏳ This may take a few minutes on first run..."

# Build and run with docker-compose
docker-compose up --build -d

# Wait for the container to be ready
echo "⏳ Waiting for the application to start..."
sleep 10

# Check if the container is running
if docker-compose ps | grep -q "Up"; then
    echo "✅ Student Loan Assistant is running!"
    echo "🌐 Access the application at: http://localhost:8501"
    echo ""
    echo "💡 Useful commands:"
    echo "   - View logs: docker-compose logs -f"
    echo "   - Stop app: docker-compose down"
    echo "   - Restart app: docker-compose restart"
    echo ""
    echo "🚀 Happy learning about student loans!"
else
    echo "❌ Error: Container failed to start. Check logs with:"
    echo "   docker-compose logs"
    exit 1
fi 