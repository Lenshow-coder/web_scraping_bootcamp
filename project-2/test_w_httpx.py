import httpx

url = "https://unsplash.com/napi/search/photos?page=2&per_page=20&query=water"

headers = {
    'authority': 'unsplash.com',
    'accept': '*/*',
    'accept-language': 'en-US',
    'cache-control': 'no-cache',
    'client-geo-region': 'global',
    'cookie': 'require_cookie_consent=false; xp-search-hybrid-v1=variant_a; xp-no-top-affiliates=v1; xp-purchase=button; uuid=942c507d-b7be-46b3-9164-6dcf41efca8b; azk=942c507d-b7be-46b3-9164-6dcf41efca8b; azk-ss=true; _sp_ses.0295=*; _sp_id.0295=d462046f-90cc-4de4-a664-b26fa20009da.1754959688.5.1755374643.1755052291.5e27aa8a-d154-4843-a11d-8bb7796a8cfb.8b269dcd-bbd4-499a-9131-94130f1c3b0a.a7d1fff1-718e-4010-976c-ebe3ea469245.1755374628830.9; _dd_s=aid=owwqzoybd1&logs=1&id=8d9b9824-a154-43b5-84a1-4ab8e8f7971f&created=1755374628758&expire=1755375543521',
    'pragma': 'no-cache',
    'referer': 'https://unsplash.com/s/photos/water',
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

# Use HTTP/2
with httpx.Client(http2=True) as client:
    response = client.get(url, headers=headers)
    print(f"Status: {response.status_code}")
    print(response.text[:200])