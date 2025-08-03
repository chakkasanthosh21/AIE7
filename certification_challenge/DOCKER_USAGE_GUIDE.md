# 🐳 Student Loan Assistant - Docker Usage Guide

**Complete Step-by-Step Instructions for Running the App with Docker**

---

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Getting Started](#getting-started)
3. [Step-by-Step Setup](#step-by-step-setup)
4. [Using the Application](#using-the-application)
5. [Troubleshooting](#troubleshooting)
6. [Advanced Usage](#advanced-usage)
7. [Cleanup](#cleanup)

---

## 🎯 Prerequisites

### Required Software
- **Docker Desktop** - [Download here](https://docs.docker.com/get-docker/)
- **Docker Compose** - Usually included with Docker Desktop
- **Git** - [Download here](https://git-scm.com/downloads)

### Required API Keys
- **OpenAI API Key** - [Get here](https://platform.openai.com/api-keys)
- **Cohere API Key** (Optional) - [Get here](https://dashboard.cohere.ai/api-keys)

### System Requirements
- **RAM**: Minimum 4GB, Recommended 8GB+
- **Storage**: At least 2GB free space
- **OS**: Windows 10+, macOS 10.15+, or Linux

---

## 🚀 Getting Started

### Step 1: Install Docker Desktop

#### For Windows:
1. Download Docker Desktop from [Docker's website](https://docs.docker.com/desktop/install/windows/)
2. Run the installer and follow the setup wizard
3. Restart your computer when prompted
4. Start Docker Desktop from the Start menu

#### For macOS:
1. Download Docker Desktop from [Docker's website](https://docs.docker.com/desktop/install/mac/)
2. Drag Docker to Applications folder
3. Open Docker Desktop from Applications
4. Grant necessary permissions when prompted

#### For Linux:
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install docker.io docker-compose

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Add user to docker group (optional)
sudo usermod -aG docker $USER
```

### Step 2: Verify Docker Installation
Open a terminal/command prompt and run:
```bash
# Check Docker version
docker --version

# Check Docker Compose version
docker-compose --version

# Test Docker installation
docker run hello-world
```

If you see "Hello from Docker!" message, Docker is working correctly.

---

## 📝 Step-by-Step Setup

### Step 1: Clone the Repository
```bash
# Clone the repository
git clone https://github.com/your-username/AIE7.git

# Navigate to the project directory
cd AIE7/certification_challenge

# Verify you're in the right directory
ls -la
```

You should see files like `Dockerfile`, `docker-compose.yml`, `run_docker.sh`, etc.

### Step 2: Get Your API Keys

#### OpenAI API Key:
1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key (it starts with `sk-`)
5. **Important**: Save it securely - you won't see it again!

#### Cohere API Key (Optional):
1. Go to [Cohere Dashboard](https://dashboard.cohere.ai/api-keys)
2. Sign in or create an account
3. Click "Create API Key"
4. Copy the key

### Step 3: Configure Environment Variables

#### Option A: Using the Automated Script (Recommended)
```bash
# Make the script executable
chmod +x run_docker.sh

# Run the setup script
./run_docker.sh
```

The script will:
- Create a `.env` file template
- Guide you through API key setup
- Check Docker installation
- Build and start the container

#### Option B: Manual Configuration
```bash
# Copy the environment template
cp env.template .env

# Edit the .env file with your API keys
# On macOS/Linux:
nano .env

# On Windows:
notepad .env
```

Edit the `.env` file to look like this:
```bash
# Required: OpenAI API Key
OPENAI_API_KEY=sk-your-actual-openai-key-here

# Optional: Cohere API Key
COHERE_API_KEY=your-actual-cohere-key-here

# Streamlit Configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
```

### Step 4: Build and Run the Application

#### Using Docker Compose (Recommended):
```bash
# Build and start the container
docker-compose up --build -d

# Check if it's running
docker-compose ps

# View logs
docker-compose logs -f
```

#### Using the Automated Script:
```bash
# Run the complete setup
./run_docker.sh
```

### Step 5: Access the Application
1. Open your web browser
2. Go to: **http://localhost:8501**
3. You should see the Student Loan Assistant interface

---

## 🎮 Using the Application

### Main Interface
The application has three main tabs:

#### 💬 Chat Tab
- **Ask Questions**: Type your student loan questions in the text area
- **Example Queries**: Click buttons in the sidebar for sample questions
- **Conversation History**: View your chat history below

#### 📊 Evaluation Tab
- **Run Evaluation**: Click to test system performance
- **View Metrics**: See detailed performance scores
- **Performance Analysis**: Understand system capabilities

#### 🔍 Retrieval Comparison Tab
- **Compare Methods**: Test different retrieval strategies
- **Performance Analysis**: See which method works best

### Example Questions to Try
1. "What are the eligibility requirements for federal student loans?"
2. "How do I apply for a Direct Loan?"
3. "What are the current interest rates for student loans?"
4. "How do I repay my student loans?"
5. "What happens if I can't make my loan payments?"

### Sidebar Features
- **System Status**: Check if everything is working
- **Quick Actions**: Reinitialize, evaluate, or clear history
- **Example Queries**: Pre-written questions for testing

---

## 🛠️ Troubleshooting

### Common Issues and Solutions

#### Issue 1: "Docker command not found"
**Solution:**
```bash
# Install Docker Desktop first
# Then restart your terminal/command prompt
```

#### Issue 2: "Port 8501 is already in use"
**Solution:**
```bash
# Check what's using the port
lsof -i :8501

# Stop the application
docker-compose down

# Change port in docker-compose.yml if needed
# Edit the ports section to use a different port
```

#### Issue 3: "Container failed to start"
**Solution:**
```bash
# Check logs
docker-compose logs

# Verify API keys in .env file
cat .env

# Rebuild container
docker-compose up --build -d
```

#### Issue 4: "Permission denied" on run_docker.sh
**Solution:**
```bash
# Fix permissions
chmod +x run_docker.sh
```

#### Issue 5: "API key not valid"
**Solution:**
1. Check your API key in the `.env` file
2. Verify the key is correct and active
3. Ensure you have sufficient credits in your OpenAI account

#### Issue 6: "Container keeps restarting"
**Solution:**
```bash
# Check container logs
docker-compose logs student-loan-assistant

# Check resource usage
docker stats

# Restart Docker Desktop if needed
```

### Health Check Commands
```bash
# Check if container is healthy
docker-compose ps

# View health check details
docker inspect student-loan-assistant | grep -A 10 "Health"

# Check application logs
docker-compose logs -f student-loan-assistant
```

### Resource Monitoring
```bash
# Monitor container resources
docker stats student-loan-assistant

# Check disk usage
docker system df

# View container details
docker inspect student-loan-assistant
```

---

## 🔧 Advanced Usage

### Development Mode
```bash
# Run with live code reloading
docker-compose -f docker-compose.dev.yml up -d

# Access container shell
docker-compose exec student-loan-assistant bash

# View real-time logs
docker-compose logs -f --tail=100
```

### Custom Configuration
Edit `docker-compose.yml` to customize:

#### Change Port:
```yaml
ports:
  - "8080:8501"  # Use port 8080 instead of 8501
```

#### Add Environment Variables:
```yaml
environment:
  - OPENAI_API_KEY=${OPENAI_API_KEY}
  - COHERE_API_KEY=${COHERE_API_KEY}
  - CUSTOM_VAR=value
```

#### Modify Resource Limits:
```yaml
deploy:
  resources:
    limits:
      memory: 2G
      cpus: '1.0'
```

### Production Deployment
```bash
# Use production configuration
docker-compose -f docker-compose.prod.yml up -d

# Set up monitoring
docker-compose -f docker-compose.monitoring.yml up -d
```

### Backup and Restore
```bash
# Backup data
docker-compose exec student-loan-assistant tar -czf /app/backup.tar.gz /app/data

# Copy backup from container
docker cp student-loan-assistant:/app/backup.tar.gz ./backup.tar.gz

# Restore data
docker cp ./backup.tar.gz student-loan-assistant:/app/
docker-compose exec student-loan-assistant tar -xzf /app/backup.tar.gz -C /app/
```

---

## 🧹 Cleanup

### Stop the Application
```bash
# Stop and remove containers
docker-compose down

# Stop and remove everything (including images)
docker-compose down --rmi all
```

### Remove Docker Resources
```bash
# Remove unused containers
docker container prune

# Remove unused images
docker image prune

# Remove unused volumes
docker volume prune

# Remove everything unused
docker system prune -a
```

### Complete Cleanup
```bash
# Stop all containers
docker stop $(docker ps -a -q)

# Remove all containers
docker rm $(docker ps -a -q)

# Remove all images
docker rmi $(docker images -q)

# Remove all volumes
docker volume rm $(docker volume ls -q)
```

---

## 📞 Support

### Getting Help
1. **Check this guide** for common solutions
2. **View application logs**: `docker-compose logs`
3. **Check container status**: `docker-compose ps`
4. **Review the main README**: For application details

### Useful Commands Reference
```bash
# Basic operations
docker-compose up -d          # Start application
docker-compose down           # Stop application
docker-compose restart        # Restart application
docker-compose logs -f        # View logs
docker-compose ps             # Check status

# Development
docker-compose exec student-loan-assistant bash  # Access shell
docker-compose up --build -d  # Rebuild and start
docker stats student-loan-assistant              # Monitor resources

# Troubleshooting
docker-compose logs --tail=100  # Last 100 log lines
docker inspect student-loan-assistant  # Container details
docker system prune -a          # Clean up everything
```

### Resources
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [OpenAI API Documentation](https://platform.openai.com/docs/)

---

## 🎉 Success!

Once you've completed these steps, you should have:
- ✅ **Student Loan Assistant** running at http://localhost:8501
- ✅ **Multi-agent AI system** ready to answer questions
- ✅ **Advanced RAG capabilities** with multiple retrieval methods
- ✅ **Beautiful web interface** for interaction
- ✅ **Performance evaluation** tools
- ✅ **Production-ready** Docker deployment

**Happy learning about student loans! 🎓✨**

---

*This guide covers everything you need to run the Student Loan Assistant with Docker. If you encounter any issues not covered here, please check the troubleshooting section or refer to the main documentation.* 