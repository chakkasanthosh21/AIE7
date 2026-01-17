# 🐳 Student Loan Assistant - Docker Usage Guide

This guide provides step-by-step instructions for running the Student Loan Assistant using Docker.

## 📋 Prerequisites

Before running the application, ensure you have:

- **Docker** installed on your system
- **Docker Compose** (optional, for easier management)
- **Git** (to clone the repository)
- **API Keys** for the services you want to use

### Required API Keys:
- **OpenAI API Key** (Required) - Get from [OpenAI Platform](https://platform.openai.com/api-keys)
- **Cohere API Key** (Optional) - Get from [Cohere Dashboard](https://dashboard.cohere.ai/api-keys)
- **Tavily API Key** (Optional) - Get from [Tavily](https://tavily.com/)

## 🚀 Quick Start

### Method 1: Using Docker Run (Recommended)

1. **Clone the repository** (if not already done):
   ```bash
   git clone https://github.com/your-username/AIE7.git
   cd AIE7/certification_challenge
   ```

2. **Build the Docker image**:
   ```bash
   docker build -t student-loan-assistant .
   ```

3. **Run the container**:
   ```bash
   docker run -p 8501:8501 --name student-loan-app student-loan-assistant
   ```

4. **Access the application**:
   - Open your browser and go to: `http://localhost:8501`
   - The app will be ready to use!

### Method 2: Using Docker Compose

1. **Create a docker-compose.yml file** (if not exists):
   ```yaml
   version: '3.8'
   
   services:
     student-loan-assistant:
       build: .
       ports:
         - "8501:8501"
       container_name: student-loan-app
       restart: unless-stopped
       environment:
         - STREAMLIT_SERVER_PORT=8501
         - STREAMLIT_SERVER_ADDRESS=0.0.0.0
   ```

2. **Run with Docker Compose**:
   ```bash
   docker-compose up -d
   ```

3. **Access the application**:
   - Open your browser and go to: `http://localhost:8501`

## 🔧 Advanced Usage

### Custom Port Configuration

If you want to run the app on a different port:

```bash
# Using Docker run
docker run -p 8080:8501 --name student-loan-app student-loan-assistant

# Using Docker Compose (update docker-compose.yml)
ports:
  - "8080:8501"
```

### Environment Variables

You can set environment variables for the container:

```bash
docker run -p 8501:8501 \
  -e OPENAI_API_KEY=your_openai_key \
  -e COHERE_API_KEY=your_cohere_key \
  -e TAVILY_API_KEY=your_tavily_key \
  --name student-loan-app \
  student-loan-assistant
```

### Volume Mounting (for Development)

To mount the source code for development:

```bash
docker run -p 8501:8501 \
  -v $(pwd):/app \
  --name student-loan-app \
  student-loan-assistant
```

## 📱 Using the Application

### 1. Initial Setup
- Open `http://localhost:8501` in your browser
- You'll see the API Key Configuration page

### 2. Configure API Keys
- **Required**: Enter your OpenAI API Key
- **Optional**: Enter Cohere API Key (for enhanced retrieval)
- **Optional**: Enter Tavily API Key (for real-time web search)
- Click "🚀 Start Chatbot"

### 3. Start Chatting
- The chatbot interface will appear immediately
- Ask questions about student loans
- Use the quick question buttons in the sidebar

## 🛠️ Troubleshooting

### Common Issues

#### 1. Port Already in Use
```bash
# Check what's using port 8501
lsof -i :8501

# Kill the process or use a different port
docker run -p 8502:8501 --name student-loan-app student-loan-assistant
```

#### 2. Container Won't Start
```bash
# Check container logs
docker logs student-loan-app

# Remove and recreate container
docker rm -f student-loan-app
docker run -p 8501:8501 --name student-loan-app student-loan-assistant
```

#### 3. Build Issues
```bash
# Clean build (no cache)
docker build --no-cache -t student-loan-assistant .

# Check Dockerfile syntax
docker build --dry-run -t student-loan-assistant .
```

#### 4. Permission Issues
```bash
# Run with proper permissions
docker run -p 8501:8501 --user $(id -u):$(id -g) --name student-loan-app student-loan-assistant
```

### Health Check

The container includes a health check. You can monitor it:

```bash
# Check container health
docker ps

# View health check logs
docker inspect student-loan-app | grep -A 10 "Health"
```

## 🔒 Security Considerations

### API Key Security
- **Never commit API keys** to version control
- Use environment variables or Docker secrets
- Consider using a secrets management service

### Network Security
- The app runs on `0.0.0.0` inside the container
- Only expose necessary ports
- Consider using a reverse proxy for production

### Example with Docker Secrets:
```bash
# Create a secret
echo "your_openai_key" | docker secret create openai_api_key -

# Run with secret
docker run -p 8501:8501 \
  --secret openai_api_key \
  --name student-loan-app \
  student-loan-assistant
```

## 📊 Monitoring and Logs

### View Application Logs
```bash
# Follow logs in real-time
docker logs -f student-loan-app

# View last 100 lines
docker logs --tail 100 student-loan-app
```

### Container Statistics
```bash
# Monitor resource usage
docker stats student-loan-app

# Detailed container info
docker inspect student-loan-app
```

## 🚀 Production Deployment

### Using Docker Swarm
```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml student-loan-stack
```

### Using Kubernetes
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: student-loan-assistant
spec:
  replicas: 3
  selector:
    matchLabels:
      app: student-loan-assistant
  template:
    metadata:
      labels:
        app: student-loan-assistant
    spec:
      containers:
      - name: student-loan-assistant
        image: student-loan-assistant:latest
        ports:
        - containerPort: 8501
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: openai-secret
              key: api-key
```

## 🧹 Cleanup

### Stop and Remove Container
```bash
# Stop container
docker stop student-loan-app

# Remove container
docker rm student-loan-app

# Remove image
docker rmi student-loan-assistant
```

### Using Docker Compose
```bash
# Stop and remove containers
docker-compose down

# Remove images
docker-compose down --rmi all
```

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review the application logs: `docker logs student-loan-app`
3. Verify your API keys are correct
4. Ensure Docker has sufficient resources allocated

## 🎯 Quick Commands Reference

```bash
# Build image
docker build -t student-loan-assistant .

# Run container
docker run -p 8501:8501 --name student-loan-app student-loan-assistant

# Stop container
docker stop student-loan-app

# Remove container
docker rm student-loan-app

# View logs
docker logs -f student-loan-app

# Access container shell
docker exec -it student-loan-app /bin/bash

# Check container status
docker ps -a
```

---

**🎓 Your Student Loan Assistant is now ready to help users navigate federal loan programs!** 