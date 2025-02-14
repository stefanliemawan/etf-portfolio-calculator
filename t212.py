import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("T212_API_KEY")
print(API_KEY)

url = "https://demo.trading212.com/api/v0/equity/pies"

headers = {"Authorization": "API_KEY"}

response = requests.get(url, headers=headers)
print(response)
data = response.json()
print(data)
