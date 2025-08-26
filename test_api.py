import requests
from config import API_KEY

BASE_URL = "https://www.alphavantage.co/query"
params = {
    "function": "OVERVIEW",
    "symbol": "IBM",
    "apikey": API_KEY
}

# making requests
def test_something():
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        print("✅ API call successful.")
        data = response.json()
        print(f"Company: {data.get('Name')}")
        print(f"Description: {data.get('Description')[:103]}...") #just printing first 103 characters eh
    else:
        print(f"❌ API call failed with status code {response.status_code}")
        print(response.text)