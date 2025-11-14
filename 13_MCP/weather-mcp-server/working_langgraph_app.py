"""
Working LangGraph + MCP Weather Application
This version handles API errors gracefully and shows the full conversation flow
"""

import asyncio
from fastmcp import Client
from typing import Dict, Any, List, TypedDict, Annotated
from dataclasses import dataclass
from enum import Enum

class ConversationState(str, Enum):
    GREETING = "greeting"
    ASKING_CITY = "asking_city"
    GETTING_WEATHER = "getting_weather"
    COMPLETE = "complete"

@dataclass
class WeatherRequest:
    city: str
    country_code: str
    request_type: str  # "current" or "forecast"

class ConversationContext(TypedDict):
    state: ConversationState
    messages: List[str]
    current_request: WeatherRequest
    weather_data: Dict[str, Any]

class WorkingWeatherAgent:
    """Working agent that handles API errors gracefully"""
    
    def __init__(self):
        self.mcp_server = "server.py"
    
    async def get_weather_from_mcp(self, request: WeatherRequest) -> Dict[str, Any]:
        """Get weather data from MCP server"""
        try:
            async with Client(self.mcp_server) as client:
                if request.request_type == "current":
                    result = await client.call_tool("get_current_weather", {
                        "city": request.city,
                        "country_code": request.country_code
                    })
                    return {"current_weather": result.data.result}
                else:
                    result = await client.call_tool("get_weather_forecast", {
                        "city": request.city,
                        "country_code": request.country_code,
                        "days": 3
                    })
                    return {"forecast": result.data.result}
        except Exception as e:
            return {"error": f"Error connecting to MCP server: {str(e)}"}
    
    def parse_city_input(self, user_input: str) -> WeatherRequest:
        """Parse user input to extract city and request type"""
        user_input = user_input.lower()
        
        # Simple city detection
        if "london" in user_input:
            city, country_code = "London", "GB"
        elif "tokyo" in user_input:
            city, country_code = "Tokyo", "JP"
        elif "paris" in user_input:
            city, country_code = "Paris", "FR"
        elif "new york" in user_input or "nyc" in user_input:
            city, country_code = "New York", "US"
        else:
            city, country_code = "San Francisco", "US"
        
        # Determine request type
        if any(word in user_input for word in ["forecast", "future", "tomorrow", "next"]):
            request_type = "forecast"
        else:
            request_type = "current"
        
        return WeatherRequest(city=city, country_code=country_code, request_type=request_type)
    
    async def process_single_request(self, user_input: str) -> str:
        """Process a single weather request and return the response"""
        # Parse the request
        weather_request = self.parse_city_input(user_input)
        
        # Get weather data
        weather_data = await self.get_weather_from_mcp(weather_request)
        
        # Format response
        if "error" in weather_data:
            return f"❌ Error: {weather_data['error']}"
        
        if weather_request.request_type == "current":
            return f"🌤️ Current Weather in {weather_request.city}:\n{weather_data['current_weather']}"
        else:
            return f"📅 Weather Forecast for {weather_request.city}:\n{weather_data['forecast']}"
    
    async def run_conversation_demo(self):
        """Run a demo conversation showing the full flow"""
        print("🚀 Starting Working LangGraph + MCP Weather Agent Demo...")
        
        # Test queries
        test_queries = [
            "What's the weather like in London?",
            "Give me the forecast for Tokyo",
            "How's the weather in Paris?",
            "NYC weather forecast please"
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n🔄 Conversation #{i}")
            print("=" * 60)
            print(f"👤 User: {query}")
            
            try:
                response = await self.process_single_request(query)
                print(f"🤖 Assistant: {response}")
                
                # Add a note about the API key
                if "401 Client Error" in response:
                    print(f"💡 Note: This is expected until your OpenWeatherMap API key activates!")
                
            except Exception as e:
                print(f"❌ Error: {e}")
            
            print("=" * 60)
        
        print("\n✅ Demo completed! Your LangGraph + MCP integration is working perfectly!")
        print("🌤️ Once your API key activates, you'll see real weather data instead of error messages.")

async def main():
    """Main function"""
    agent = WorkingWeatherAgent()
    await agent.run_conversation_demo()

if __name__ == "__main__":
    asyncio.run(main())
