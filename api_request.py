import requests

base_url = "http://127.0.0.1:5000/process-text"

params = {
    "text": "Hello World",
    "duplication_factor": 3,
    "capitalization": "UPPER"
}

response = requests.get(base_url, params=params)
print(response.json())