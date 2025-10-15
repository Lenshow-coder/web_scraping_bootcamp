import pandas as pd
import pycurl
import io
import json
import os
from httpx import get

def get_headers(query):
    """Convert headers dictionary to pycurl format"""
    headers = [
        'authority: unsplash.com',
        'accept: */*',
        'accept-language: en-US',
        'cache-control: no-cache',
        'client-geo-region: global',
        'cookie: require_cookie_consent=false; xp-search-hybrid-v1=variant_a; xp-no-top-affiliates=v1; xp-purchase=button; uuid=942c507d-b7be-46b3-9164-6dcf41efca8b; azk=942c507d-b7be-46b3-9164-6dcf41efca8b; azk-ss=true; _sp_ses.0295=*; _sp_id.0295=d462046f-90cc-4de4-a664-b26fa20009da.1754959688.3.1755041181.1755028007.2a4564b2-f9dc-4d2c-a607-c8db01b9cdb3.4a94104f-9afe-4cee-be7f-fd3911d0d830.f8de1b92-093b-41a4-abf4-dd1e989728f2.1755040222516.35; _dd_s=aid=owwqzoybd1&logs=1&id=075ed5ce-ac27-4c3f-8e76-051458ed5568&created=1755040223128&expire=1755042085094',
        'pragma: no-cache',
        f'referer: https://unsplash.com/s/photos/{query}',
        'sec-ch-ua: "Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        'sec-ch-ua-mobile: ?0',
        'sec-ch-ua-platform: "Windows"',
        'sec-fetch-dest: empty',
        'sec-fetch-mode: cors',
        'sec-fetch-site: same-origin',
        'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    ]
    return headers

def make_request(url, headers=None):
    """Make HTTP request using pycurl"""
    buffer = io.BytesIO()
    
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEDATA, buffer)
    c.setopt(c.HTTPHEADER, headers)
    
    # Perform the request
    c.perform()
    status_code = c.getinfo(c.RESPONSE_CODE)
    c.close()
    
    # Debug: Check response status and content
    print(f"Status Code: {status_code}")
    response_text = buffer.getvalue().decode('utf-8')
    print(f"Response Text (first 500 chars): {response_text[:500]}")
    
    # Create a mock response object to maintain compatibility
    class MockResponse:
        def __init__(self, text, status_code):
            self.text = text
            self.status_code = status_code
    
    return MockResponse(response_text, status_code)

def parse_response(response):
    """Parse JSON response"""
    data = json.loads(response.text)
    return data

def process_photos(data):
    """Process photos data and create DataFrame"""
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
    """Save DataFrame to CSV"""
    df.to_csv("photos2.csv", index=False)

def scrape(query, results, page=1):
    """Main scraping function"""
    
    success_count = 0

    while success_count < results:
        url = f"https://unsplash.com/napi/search/photos?page={page}&per_page=10&query={query}&xp=search-hybrid-v1%3Avariant_a"

        headers = get_headers(query)
        response = make_request(url, headers)
        data = parse_response(response)
        max_downloads = results - success_count

        if data:
            df = process_photos(data)
            success_downloads = download_images(df["url"].tolist(), max_downloads, "images", query, page)
            success_count += success_downloads
            page += 1
        else:
            print("Error: no data returned")
            break

def download_images(img_urls, max_download, dest_dir="images", tag="", page=1):
    successfully_downloaded = 0
    for url in img_urls:
        if successfully_downloaded < max_download:
            resp = get(url)
            file = "pg_" + str(page) + "_" + "img_" + str(successfully_downloaded + 1)
            file_name = file
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
            with open(f"{dest_dir}/{tag}_{file_name}.jpeg", "wb") as f:
                f.write(resp.content)
                successfully_downloaded += 1
        else:
            break
    return successfully_downloaded

if __name__ == "__main__":
    scrape("football", 20)