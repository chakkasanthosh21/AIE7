<p align = "center" draggable=”false” ><img src="https://github.com/AI-Maker-Space/LLM-Dev-101/assets/37101144/d1343317-fa2f-41e1-8af1-1dbb18399719" 
     width="200px"
     height="auto"/>
</p>

# 13_MCP - Model Context Protocol (MCP) Integration

This directory contains the implementation of **Activity #1** and **Activity #2** from the AIE7 course, demonstrating MCP (Model Context Protocol) integration with AI applications.

## 🏗️ Directory Structure

### **AIE7-MCP-Session/** - Activity #1: Calculator MCP App
- `server.py` - Main MCP server with calculator and dice rolling tools
- `test_server.py` - Test script for the calculator app
- `dice_roller.py` - Dice rolling tool implementation
- `pyproject.toml` - Project dependencies
- `README.md` - Detailed setup and usage instructions

### **weather-mcp-server/** - Activity #2: LangGraph + MCP Integration
- `server.py` - Weather MCP server with current weather and forecast tools
- `working_langgraph_app.py` - Production-ready LangGraph + MCP integration
- `simple_langgraph_mcp.py` - Simple demo of LangGraph + MCP
- `test_weather.py` - Test script for weather MCP server
- `requirements.txt` - Python dependencies
- `README.md` - Weather server documentation

## 🎯 What Each Activity Demonstrates

### **Activity #1: Calculator MCP App**
- Building a basic MCP server with mathematical tools
- Calculator tool for evaluating expressions
- Dice rolling tool for random number generation
- Testing MCP tools locally

### **Activity #2: LangGraph + MCP Integration**
- Integrating MCP servers with LangGraph applications
- Building conversational AI agents that use local tools
- State management and conversation flow
- Error handling and graceful degradation

## 🚀 Quick Start

### **Test Calculator App (Activity #1):**
```bash
cd AIE7-MCP-Session
python3 test_server.py
```

### **Test Weather MCP Server (Activity #2):**
```bash
cd weather-mcp-server
python3 test_weather.py
```

### **Test LangGraph Integration (Activity #2):**
```bash
cd weather-mcp-server
python3 working_langgraph_app.py
```

## 🔑 Prerequisites

- Python 3.8+
- Required packages (see individual `requirements.txt` files)
- OpenWeatherMap API key (for weather functionality)
- OpenAI API key (for LangGraph LLM integration)

## 📚 Key Learning Outcomes

1. **MCP Protocol**: Understanding and implementing Model Context Protocol
2. **Local Tool Access**: Building AI agents that can use local services
3. **LangGraph Integration**: Combining conversation management with tool access
4. **Error Handling**: Building resilient applications that degrade gracefully
5. **Production Readiness**: Creating applications ready for real-world use

---

**🎉 These activities demonstrate modern AI application architecture using MCP for local tool access and LangGraph for intelligent conversation management!**
