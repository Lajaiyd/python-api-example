import requests

base_url = "https://127.0.0.1:5000/process-text"

params = {
    "text": "Hello World",
    "duplication_factor": 30,
    "capitalization": "UPPER"
}

response = requests.get(base_url, params=params)
print(response.json())