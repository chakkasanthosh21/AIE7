# 🐳 Student Loan Assistant - Docker Deployment

This guide will help you run the Student Loan Assistant using Docker, making it easy for anyone to deploy and use the application locally.

## 🚀 Quick Start

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) installed
- [Docker Compose](https://docs.docker.com/compose/install/) installed
- OpenAI API key (required)
- Cohere API key (optional, for enhanced retrieval)

### Step 1: Get API Keys
1. **OpenAI API Key**: Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. **Cohere API Key**: Visit [Cohere Dashboard](https://dashboard.cohere.ai/api-keys) (optional)

### Step 2: Clone and Setup
```bash
# Clone the repository
git clone <your-repo-url>
cd AIE7/certification_challenge

# Make the Docker runner executable
chmod +x run_docker.sh
```

### Step 3: Configure Environment
```bash
# Run the Docker setup script
./run_docker.sh
```

The script will:
- Create a `.env` file template if it doesn't exist
- Check for required dependencies
- Copy necessary data files
- Build and start the Docker container

### Step 4: Access the Application
Once the container is running, access the application at:
**http://localhost:8501**

## 📋 Manual Setup (Alternative)

### 1. Create Environment File
Create a `.env` file in the project directory:
```bash
# API Keys (Required)
OPENAI_API_KEY=your_actual_openai_api_key_here
COHERE_API_KEY=your_actual_cohere_api_key_here

# Optional: Customize these if needed
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

### 2. Build and Run with Docker Compose
```bash
# Build and start the container
docker-compose up --build -d

# Check if it's running
docker-compose ps

# View logs
docker-compose logs -f
```

### 3. Access the Application
Open your browser and go to: **http://localhost:8501**

## 🛠️ Docker Commands

### Basic Operations
```bash
# Start the application
docker-compose up -d

# Stop the application
docker-compose down

# Restart the application
docker-compose restart

# View logs
docker-compose logs -f

# Check status
docker-compose ps
```

### Development Commands
```bash
# Rebuild the container (after code changes)
docker-compose up --build -d

# Access container shell
docker-compose exec student-loan-assistant bash

# View container resources
docker stats student-loan-assistant
```

### Cleanup Commands
```bash
# Stop and remove containers
docker-compose down

# Remove containers, networks, and images
docker-compose down --rmi all

# Remove all unused Docker resources
docker system prune -a
```

## 🔧 Configuration Options

### Environment Variables
You can customize the application by modifying the `.env` file:

```bash
# Required
OPENAI_API_KEY=your_openai_key

# Optional
COHERE_API_KEY=your_cohere_key
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
```

### Port Configuration
To change the port, modify the `docker-compose.yml` file:
```yaml
ports:
  - "YOUR_PORT:8501"  # Change YOUR_PORT to desired port
```

### Data Persistence
The application mounts the following volumes:
- `./data:/app/data` - Application data
- `./logs:/app/logs` - Application logs

## 🐛 Troubleshooting

### Common Issues

#### 1. Port Already in Use
```bash
# Check what's using port 8501
lsof -i :8501

# Stop the application
docker-compose down

# Change port in docker-compose.yml if needed
```

#### 2. Container Won't Start
```bash
# Check logs
docker-compose logs

# Check if API keys are set correctly
cat .env

# Rebuild container
docker-compose up --build -d
```

#### 3. Missing Dependencies
```bash
# Rebuild with no cache
docker-compose build --no-cache

# Pull latest base image
docker pull python:3.10-slim
```

#### 4. Permission Issues
```bash
# Fix file permissions
chmod +x run_docker.sh
chmod 644 .env
```

### Health Checks
The container includes health checks. Monitor them with:
```bash
# Check health status
docker-compose ps

# View health check logs
docker inspect student-loan-assistant | grep -A 10 "Health"
```

## 📊 Monitoring

### View Application Logs
```bash
# Follow logs in real-time
docker-compose logs -f

# View last 100 lines
docker-compose logs --tail=100
```

### Resource Usage
```bash
# Monitor container resources
docker stats student-loan-assistant

# View container details
docker inspect student-loan-assistant
```

## 🔒 Security Considerations

### API Key Security
- Never commit API keys to version control
- Use environment variables for sensitive data
- Rotate API keys regularly
- Monitor API usage and costs

### Network Security
- The application runs on localhost by default
- For production, consider using HTTPS
- Implement proper authentication if needed

## 🚀 Production Deployment

### For Production Use
1. **Use HTTPS**: Configure SSL certificates
2. **Add Authentication**: Implement user authentication
3. **Monitor Resources**: Set up monitoring and alerting
4. **Backup Data**: Implement regular backups
5. **Scale**: Use Docker Swarm or Kubernetes for scaling

### Environment-Specific Configurations
```bash
# Development
docker-compose -f docker-compose.yml up -d

# Production (with custom config)
docker-compose -f docker-compose.prod.yml up -d
```

## 📞 Support

### Getting Help
1. Check the troubleshooting section above
2. View application logs: `docker-compose logs`
3. Check container status: `docker-compose ps`
4. Review the main README.md for application details

### Useful Resources
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Streamlit Documentation](https://docs.streamlit.io/)

## 🎉 Success!

Once the application is running, you can:
- Ask questions about student loans
- Test the multi-agent system
- Explore advanced retrieval methods
- View performance metrics
- Experience the complete AI application

**Happy learning about student loans! 🎓✨** 