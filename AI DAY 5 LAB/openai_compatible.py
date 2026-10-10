import requests
import json

URL = "http://localhost:11434/v1/chat/completions"
MODEL = "mess-assistant:latest"

payload = {
    "model": MODEL,
    "messages": [
        {
            "role": "system",
            "content": (
                "You are a pirate assistant. "
                "Reply in a playful pirate style. "
                "For this request, follow this system prompt."
            )
        },
        {
            "role": "user",
            "content": "What are your responsibilities?"
        }
    ],
    "stream": False,
    "temperature": 0.3
}

try:
    response = requests.post(URL, json=payload, timeout=120)
    response.raise_for_status()
    data = response.json()

    print("=== OpenAI-Compatible API Test ===")
    print("Model:", data.get("model", MODEL))
    print("Response:")
    print(data["choices"][0]["message"]["content"])

except requests.RequestException as error:
    print("API request failed:", error)
except (KeyError, IndexError, json.JSONDecodeError) as error:
    print("Could not read the response:", error)