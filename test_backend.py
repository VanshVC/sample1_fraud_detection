import requests
import json

url = "https://sample1-fraud-detection.onrender.com/api/predict"
data = {
    "amount": 100.0,
    "time": 10,
    "category": "shopping_net",
    "age": 25,
    "location": "US",
    "previous_trans": 0
}

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print("Response Body:")
    print(response.text)
except Exception as e:
    print(f"Error: {e}")
