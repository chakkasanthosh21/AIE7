#!/bin/bash

# Student Loan Assistant - Docker Runner Script
# This script makes it easy to build and run the Student Loan Assistant

set -e

echo "🎓 Student Loan Assistant - Docker Setup"
echo "========================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
check_docker() {
    print_status "Checking Docker installation..."
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        print_status "Visit: https://docs.docker.com/get-docker/"
        exit 1
    fi
    
    if ! docker info &> /dev/null; then
        print_error "Docker is not running. Please start Docker Desktop."
        exit 1
    fi
    
    print_success "Docker is installed and running"
}

# Check if Docker Compose is available
check_docker_compose() {
    print_status "Checking Docker Compose..."
    if command -v docker-compose &> /dev/null; then
        DOCKER_COMPOSE_CMD="docker-compose"
        print_success "Docker Compose found"
    elif docker compose version &> /dev/null; then
        DOCKER_COMPOSE_CMD="docker compose"
        print_success "Docker Compose (v2) found"
    else
        print_warning "Docker Compose not found, will use docker run instead"
        DOCKER_COMPOSE_CMD=""
    fi
}

# Stop existing container
stop_existing() {
    print_status "Checking for existing containers..."
    if docker ps -q -f name=student-loan-app | grep -q .; then
        print_status "Stopping existing container..."
        docker stop student-loan-app
        docker rm student-loan-app
        print_success "Existing container stopped and removed"
    fi
}

# Build the Docker image
build_image() {
    print_status "Building Docker image..."
    docker build -t student-loan-assistant .
    print_success "Docker image built successfully"
}

# Run with Docker Compose
run_with_compose() {
    print_status "Starting with Docker Compose..."
    $DOCKER_COMPOSE_CMD up -d
    print_success "Container started with Docker Compose"
}

# Run with Docker run
run_with_docker() {
    print_status "Starting with Docker run..."
    docker run -d \
        --name student-loan-app \
        -p 8501:8501 \
        --restart unless-stopped \
        student-loan-assistant
    print_success "Container started with Docker run"
}

# Wait for application to be ready
wait_for_app() {
    print_status "Waiting for application to start..."
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s http://localhost:8501 > /dev/null 2>&1; then
            print_success "Application is ready!"
            return 0
        fi
        
        print_status "Attempt $attempt/$max_attempts - Waiting for application..."
        sleep 2
        attempt=$((attempt + 1))
    done
    
    print_warning "Application may still be starting. Please check manually."
    return 1
}

# Show status
show_status() {
    echo ""
    echo "🎯 Application Status"
    echo "===================="
    
    if docker ps -q -f name=student-loan-app | grep -q .; then
        print_success "Container is running"
        echo "📊 Container details:"
        docker ps -f name=student-loan-app --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    else
        print_error "Container is not running"
    fi
    
    echo ""
    echo "🌐 Access Information"
    echo "===================="
    echo "Local URL:  http://localhost:8501"
    echo "Network URL: http://$(hostname -I | awk '{print $1}'):8501"
    
    echo ""
    echo "📋 Next Steps"
    echo "============="
    echo "1. Open your browser and go to: http://localhost:8501"
    echo "2. Enter your OpenAI API key (required)"
    echo "3. Optionally enter Cohere and Tavily API keys"
    echo "4. Click '🚀 Start Chatbot' to begin"
    
    echo ""
    echo "🔧 Useful Commands"
    echo "=================="
    echo "View logs:     docker logs -f student-loan-app"
    echo "Stop app:      docker stop student-loan-app"
    echo "Restart app:   docker restart student-loan-app"
    echo "Remove app:    docker rm -f student-loan-app"
}

# Main execution
main() {
    echo ""
    check_docker
    check_docker_compose
    stop_existing
    build_image
    
    if [ -n "$DOCKER_COMPOSE_CMD" ]; then
        run_with_compose
    else
        run_with_docker
    fi
    
    wait_for_app
    show_status
}

# Handle script arguments
case "${1:-}" in
    "stop")
        print_status "Stopping Student Loan Assistant..."
        if [ -n "$DOCKER_COMPOSE_CMD" ]; then
            $DOCKER_COMPOSE_CMD down
        else
            docker stop student-loan-app 2>/dev/null || true
            docker rm student-loan-app 2>/dev/null || true
        fi
        print_success "Application stopped"
        ;;
    "restart")
        print_status "Restarting Student Loan Assistant..."
        if [ -n "$DOCKER_COMPOSE_CMD" ]; then
            $DOCKER_COMPOSE_CMD restart
        else
            docker restart student-loan-app
        fi
        print_success "Application restarted"
        ;;
    "logs")
        print_status "Showing application logs..."
        docker logs -f student-loan-app
        ;;
    "status")
        show_status
        ;;
    "clean")
        print_status "Cleaning up Docker resources..."
        if [ -n "$DOCKER_COMPOSE_CMD" ]; then
            $DOCKER_COMPOSE_CMD down --rmi all --volumes --remove-orphans
        else
            docker stop student-loan-app 2>/dev/null || true
            docker rm student-loan-app 2>/dev/null || true
            docker rmi student-loan-assistant 2>/dev/null || true
        fi
        print_success "Cleanup completed"
        ;;
    "help"|"-h"|"--help")
        echo "🎓 Student Loan Assistant - Docker Runner"
        echo ""
        echo "Usage: $0 [COMMAND]"
        echo ""
        echo "Commands:"
        echo "  (no args)  Build and start the application"
        echo "  stop       Stop the application"
        echo "  restart    Restart the application"
        echo "  logs       Show application logs"
        echo "  status     Show application status"
        echo "  clean      Clean up all Docker resources"
        echo "  help       Show this help message"
        echo ""
        echo "Examples:"
        echo "  $0          # Start the application"
        echo "  $0 stop     # Stop the application"
        echo "  $0 logs     # View logs"
        ;;
    "")
        main
        ;;
    *)
        print_error "Unknown command: $1"
        echo "Use '$0 help' for usage information"
        exit 1
        ;;
esac 