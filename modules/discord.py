import time
import requests


def send_to_discord(webhook_url, message):
    headers = {"Content-Type": "application/json"}
    data = {"content": f"```{message}```"}
    response = requests.post(webhook_url, headers=headers, data=json.dumps(data))

    # Simple rate limiting (if necessary)
    if response.status_code == 429:
        print("Rate limit exceeded, retrying after delay...")
        time.sleep(5)  # Retry after 5 seconds
        response = requests.post(webhook_url, headers=headers, data=json.dumps(data))

    if response.status_code == 204:
        print("Result sent to Discord successfully!")
    else:
        print(f"Failed to send to Discord: {response.status_code} - {response.text}")
