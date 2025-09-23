import pandas as pd
import requests
import json

def scrape(query, results):
    url = f"https://unsplash.com/s/photos/{query}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    print(data)




if __name__ == "__main__":
    scrape("water", 10)