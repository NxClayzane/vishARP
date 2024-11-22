import requests
import json

def send_to_discord(webhook_url, message):
    headers = {"Content-Type": "application/json"}
    data = {"content": f"```{message}```"}
    response = requests.post(webhook_url, headers=headers, data=json.dumps(data))
    if response.status_code == 204:
        print("Result sent to Discord successfully!")
    else:
        print(f"Failed to send to Discord: {response.status_code} - {response.text}")
