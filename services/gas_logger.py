import requests
import os

GAS_URL = os.getenv("GAS_WEBHOOK_URL")

def log_to_google(user_id: int, command: str):
    if not GAS_URL:
        print("GAS URL is not set")
        return

    data = {
        "user_id": user_id,
        "command": command
    }

    try:
        response = requests.post(GAS_URL, json=data)
        if response.status_code != 200:
            print(f"Logging failed: {response.status_code} {response.text}")
    except Exception as e:
        print(f"Logging failed: {e}")