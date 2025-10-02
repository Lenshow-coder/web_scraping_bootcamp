import requests

url = "https://api.higherme.com/classic/jobs?page=1&includes=location,location.company,location.externalServiceReferences&limit=24&filters\\[brand.id\\]=58bd9e7f472bd&filters\\[lat\\]=43.70643&filters\\[lng\\]=-79.39864&filters\\[distance\\]=20&sort\\[distance\\]=asc"

payload = {}
headers = {
  'authority': 'api.higherme.com',
  'accept': 'application/json, text/plain, */*',
  'accept-language': 'en-US,en;q=0.9',
  'higherme-client-version': '2028.08.08_23.0d',
  'origin': 'https://app.higherme.com',
  'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-site',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
