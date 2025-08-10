# 🌤️ Weather MCP Server

A Model Context Protocol (MCP) server that provides weather information using the OpenWeatherMap API.

## 🚀 Features

- **Current Weather**: Get real-time weather for any city
- **Weather Forecast**: Get 5-day weather forecasts
- **Beautiful Formatting**: Emoji-rich, easy-to-read weather reports
- **Error Handling**: Graceful error handling for API issues

## 📋 Prerequisites

1. **Python 3.7+**
2. **OpenWeatherMap API Key** (free at [openweathermap.org/api](https://openweathermap.org/api))

## 🛠️ Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Get API Key
1. Go to [OpenWeatherMap](https://openweathermap.org/api)
2. Sign up for a free account
3. Get your API key

### 3. Configure Environment
Edit the `.env` file and add your API key:
```bash
OPENWEATHER_API_KEY=your_actual_api_key_here
```

## 🧪 Testing

### Test the Server
```bash
python3 test_weather.py
```

### Test Individual Tools
```bash
# Test current weather
python3 -c "
from fastmcp import Client
import asyncio

async def test():
    async with Client('server.py') as client:
        result = await client.call_tool('get_current_weather', {'city': 'London'})
        print(result)

asyncio.run(test())
"
```

## 🎯 Available Tools

### `get_current_weather(city: str, country_code: str = "US")`
Get current weather for a specific city.

**Example:**
```python
result = await client.call_tool("get_current_weather", {"city": "Tokyo", "country_code": "JP"})
```

### `get_weather_forecast(city: str, country_code: str = "US", days: int = 5)`
Get weather forecast for up to 5 days.

**Example:**
```python
result = await client.call_tool("get_weather_forecast", {"city": "Paris", "days": 3})
```

## 🔧 Integration with Cursor

Add to your `~/.cursor/mcp.json`:
```json
{
  "mcpServers": {
    "weather": {
      "command": "python3",
      "args": ["server.py"],
      "cwd": "/path/to/your/weather-mcp-server"
    }
  }
}
```

## 📊 API Limits

- **Free Tier**: 1000 calls/day
- **Units**: Metric (Celsius, m/s)
- **Forecast**: Up to 5 days

## 🐛 Troubleshooting

- **API Key Error**: Make sure your `.env` file has the correct API key
- **City Not Found**: Check city name spelling and country code
- **Rate Limit**: Free tier allows 1000 calls per day

## 🎉 Enjoy Your Weather MCP Server!

Now you can get weather information directly through Cursor using MCP!
