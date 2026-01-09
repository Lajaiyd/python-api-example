import requests

base_url = "https://book-review-api-v7t4.onrender.com/process-text"

params = {
    "text": "Hello World",
    "duplication_factor": 30,
    "capitalization": "UPPER"
}

response = requests.get(base_url, params=params)
print(response.json())