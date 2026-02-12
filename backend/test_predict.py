import requests

data = {
    "amount": 100.0,
    "time": 1,
    "category": "shopping",
    "age": 30,
    "location": "NY",
    "previous_trans": 0
}

try:
    response = requests.post("http://127.0.0.1:8000/api/predict", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")
