import requests
import json
import pandas as pd

latitude = "43.70643"
longitude = "-79.39864"
results = "24"

url = "https://api.higherme.com/classic/jobs"

querystring = {"page":"1",
               "includes":"location,location.company,location.externalServiceReferences",
               "limit":results,
               "filters[brand.id]":"58bd9e7f472bd",
               "filters[lat]":latitude,
               "filters[lng]":longitude,
               "filters[distance]":"20",
               "sort[distance]":"asc"}

headers = {
    "authority": "api.higherme.com",
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "higherme-client-version": "2028.08.08_23.0d",
    "origin": "https://app.higherme.com",
    "^sec-ch-ua": "^\^Chromium^^;v=^\^122^^, ^\^NotA:Brand^^;v=^\^24^^, ^\^Google",
    "sec-ch-ua-mobile": "?0",
    "^sec-ch-ua-platform": "^\^Windows^^^",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

response = requests.request("GET", url, headers=headers, params=querystring)
data = json.loads(response.text)

jobs = data["data"]
df = pd.DataFrame()

for job in jobs:
    title = job["attributes"]["title"]
    full_time = job["attributes"]["full_time"]
    part_time = job["attributes"]["part_time"]
    distance = job["attributes"]["distance"]
    requirements = job["attributes"]["requirements"]

    new_row = pd.DataFrame([{
        "title": title,
        "full_time": full_time,
        "part_time": part_time,
        "distance": distance,
        "requirements": requirements
    }])

    df = pd.concat([df, new_row], ignore_index=True)

df.to_csv("jobs.csv", index=False)










