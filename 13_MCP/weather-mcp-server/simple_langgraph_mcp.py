"""
Simple LangGraph + MCP Integration Demo
This demonstrates how to connect LangGraph with your Weather MCP Server
"""

import asyncio
from fastmcp import Client
from typing import Dict, Any

class WeatherAgent:
    """Simple agent that uses MCP tools for weather information"""
    
    def __init__(self):
        self.mcp_server = "server.py"
    
    async def get_weather_info(self, city: str, country_code: str = "US") -> Dict[str, Any]:
        """Get comprehensive weather information for a city"""
        results = {}
        
        try:
            # Get current weather
            async with Client(self.mcp_server) as client:
                current_weather = await client.call_tool("get_current_weather", {
                    "city": city,
                    "country_code": country_code
                })
                # Fix: Use the correct response structure
                results["current_weather"] = current_weather.data.result
                
                # Get forecast
                forecast = await client.call_tool("get_weather_forecast", {
                    "city": city,
                    "country_code": country_code,
                    "days": 3
                })
                # Fix: Use the correct response structure
                results["forecast"] = forecast.data.result
                
        except Exception as e:
            results["error"] = f"Error connecting to MCP server: {str(e)}"
        
        return results
    
    async def process_weather_request(self, user_input: str) -> str:
        """Process a natural language weather request"""
        # Simple parsing - in a real app, you'd use an LLM
        city = "San Francisco"  # Default city for demo
        
        if "london" in user_input.lower():
            city = "London"
            country_code = "GB"
        elif "tokyo" in user_input.lower():
            city = "Tokyo"
            country_code = "JP"
        else:
            country_code = "US"
        
        # Get weather data
        weather_data = await self.get_weather_info(city, country_code)
        
        # Format response
        if "error" in weather_data:
            return f"❌ {weather_data['error']}"
        
        response = f"🌤️ Weather Information for {city}:\n\n"
        response += f"📍 Current Weather:\n{weather_data['current_weather']}\n\n"
        response += f"📅 3-Day Forecast:\n{weather_data['forecast']}"
        
        return response

async def main():
    """Main function to test the Weather Agent"""
    print("🚀 Starting Simple LangGraph + MCP Weather Agent...")
    
    agent = WeatherAgent()
    
    # Test the agent
    test_queries = [
        "What's the weather like in San Francisco?",
        "Tell me about London weather",
        "How's Tokyo looking today?"
    ]
    
    for query in test_queries:
        print(f"\n🤔 Query: {query}")
        print("-" * 50)
        
        try:
            response = await agent.process_weather_request(query)
            print(f"📝 Response:\n{response}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-" * 50)

if __name__ == "__main__":
    asyncio.run(main())
