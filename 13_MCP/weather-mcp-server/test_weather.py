from fastmcp import Client

async def main():
    async with Client("server.py") as client:
        tools = await client.list_tools()
        print(f"Available weather tools: {tools}")
        
        # Test current weather
        print("\n🌤️ Testing Current Weather:")
        weather = await client.call_tool("get_current_weather", {"city": "San Francisco"})
        print(f"Current weather: {weather}")
        
        # Test forecast
        print("\n📅 Testing Weather Forecast:")
        forecast = await client.call_tool("get_weather_forecast", {"city": "San Francisco", "days": 3})
        print(f"Forecast: {forecast}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
