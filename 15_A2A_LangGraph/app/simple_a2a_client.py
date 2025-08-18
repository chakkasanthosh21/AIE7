import requests
import json

API_URL = "http://localhost:10000/v1/tasks"

# Example user query
data = {
    "assistant_id": "agent",
    "messages": [
        {"role": "user", "content": "What are the latest AI developments in 2024?"}
    ]
}

response = requests.post(API_URL, headers={"Content-Type": "application/json"}, data=json.dumps(data))

print("Status Code:", response.status_code)
try:
    print("Response:", response.json())
except Exception:
    print("Raw Response:", response.text)
