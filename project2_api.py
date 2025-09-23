import pandas as pd
import requests
import json
import httpx

def get_headers(query):
    cookie_string = "require_cookie_consent=false; xp-search-hybrid-v1=variant_a; xp-no-top-affiliates=v1; xp-purchase=button; uuid=942c507d-b7be-46b3-9164-6dcf41efca8b; azk=942c507d-b7be-46b3-9164-6dcf41efca8b; azk-ss=true; _sp_ses.0295=*; _sp_id.0295=d462046f-90cc-4de4-a664-b26fa20009da.1754959688.3.1755041181.1755028007.2a4564b2-f9dc-4d2c-a607-c8db01b9cdb3.4a94104f-9afe-4cee-be7f-fd3911d0d830.f8de1b92-093b-41a4-abf4-dd1e989728f2.1755040222516.35; _dd_s=aid=owwqzoybd1&logs=1&id=075ed5ce-ac27-4c3f-8e76-051458ed5568&created=1755040223128&expire=1755042085094"

    headers = {
    'CF-IPCountry': 'US',
    'X-Forwarded-For': '1.1.1.1',
    'authority': 'unsplash.com',
    'accept': '*/*',
    'accept-language': 'en-US',
    'cache-control': 'no-cache',
    'client-geo-region': 'global',
    'cookie': cookie_string.strip(),
    'pragma': 'no-cache',
    'referer': f'https://unsplash.com/s/photos/water',
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }
    return headers

def make_request(url, headers=None):
    response = httpx.get(url, headers=headers)
    # Debug: Check response status and content
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    print(f"Response Text (first 500 chars): {response.text[:500]}")
    return response

def parse_response(response):
    data = json.loads(response.text)
    return data

def process_photos(data):
    photos = data["results"]
    df = pd.DataFrame()

    for photo in photos:
        if photo["premium"] == False:
            url = photo["urls"]["full"]
            new_row = pd.DataFrame([{
                "url": url
            }])
            df = pd.concat([df, new_row], ignore_index=True)
        else:
            continue
    
    return df

def save_to_csv(df):
    df.to_csv("photos.csv", index=False)

def scrape(query, results):
    url = f"https://unsplash.com/napi/search/photos?page=2&per_page=20&query=water&xp=search-hybrid-v1%3Avariant_a"

    headers = get_headers(query)
    response = make_request(url, headers)
    data = parse_response(response)
    df = process_photos(data)
    save_to_csv(df)


if __name__ == "__main__":
    headers = get_headers("water")
    response = make_request("https://unsplash.com/napi/search/photos?page=2&per_page=20&query=water&xp=search-hybrid-v1%3Avariant_a", headers)
    print(response.text)
    print(headers)
    # scrape("water", 20)