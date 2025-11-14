from mcp.server.fastmcp import FastMCP
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

mcp = FastMCP("weather-mcp-server")

@mcp.tool()
def get_current_weather(city: str, country_code: str = "US") -> str:
    """Get current weather for a city"""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return "Error: OpenWeather API key not found. Please set OPENWEATHER_API_KEY in .env file"
    
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": f"{city},{country_code}",
            "appid": api_key,
            "units": "metric"  # Use Celsius
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        weather_info = {
            "city": data["name"],
            "country": data["sys"]["country"],
            "temperature": f"{data['main']['temp']}°C",
            "feels_like": f"{data['main']['feels_like']}°C",
            "description": data["weather"][0]["description"],
            "humidity": f"{data['main']['humidity']}%",
            "wind_speed": f"{data['wind']['speed']} m/s",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return f"""🌤️ Weather in {weather_info['city']}, {weather_info['country']}:
🌡️ Temperature: {weather_info['temperature']} (feels like {weather_info['feels_like']})
☁️ Conditions: {weather_info['description']}
💧 Humidity: {weather_info['humidity']}
💨 Wind: {weather_info['wind_speed']}
🕐 Updated: {weather_info['timestamp']}"""
        
    except requests.exceptions.RequestException as e:
        return f"Error fetching weather data: {str(e)}"
    except KeyError as e:
        return f"Error parsing weather data: {str(e)}"

@mcp.tool()
def get_weather_forecast(city: str, country_code: str = "US", days: int = 5) -> str:
    """Get weather forecast for a city (up to 5 days)"""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return "Error: OpenWeather API key not found. Please set OPENWEATHER_API_KEY in .env file"
    
    try:
        url = f"http://api.openweathermap.org/data/2.5/forecast"
        params = {
            "q": f"{city},{country_code}",
            "appid": api_key,
            "units": "metric",
            "cnt": days * 8  # 8 readings per day
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        forecast = []
        for item in data["list"][:days]:
            date = datetime.fromtimestamp(item["dt"]).strftime("%Y-%m-%d")
            temp = f"{item['main']['temp']}°C"
            desc = item["weather"][0]["description"]
            forecast.append(f"📅 {date}: {temp}, {desc}")
        
        return f"""🌤️ {days}-Day Forecast for {city}, {country_code}:
{chr(10).join(forecast)}"""
        
    except requests.exceptions.RequestException as e:
        return f"Error fetching forecast data: {str(e)}"
    except KeyError as e:
        return f"Error parsing forecast data: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="stdio")
