import requests
import time
import random
import pandas as pd

cookies = {
    "_trackity=8b9792d0-5390-e279-c6c2-bae2ddf893cd;"
    "TOKENS={%22access_token%22:%2213afeTyco7qZWnRzmIwiUHXB5Y9MVAGN%22%2C%22expires_in%22:157680000%2C%22expires_at%22:1883098803352%2C%22guest_token%22:%2213afeTyco7qZWnRzmIwiUHXB5Y9MVAGN%22};"
    "_ga=GA1.1.485288366.1725418807; delivery_zone=Vk4wMzkwMDYwMDI=;"
    "_gcl_au=1.1.706190331.1725418811;"
    "_hjSession_522327=eyJpZCI6Ijk3MTNhN2U5LTA5YmYtNGE0YS1hMDI4LWZmYWJiYjNiZWFmNSIsImMiOjE3MjU0MTg4MTExODEsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxfQ==;"
    "__uidac=0166d7cd3b36c81950eacebff2eda3cd; __iid=749;"
    "__iid=749; __su=0;"
    "__su=0;"
    "dtdz=8440d874-495f-51ba-836c-48749845ce91;"
    "__RC=5;"
    "__R=3;"
    "_fbp=fb.1.1725418812040.652442672852389487;"
    "tiki_client_id=485288366.1725418807;"
    "_hjSessionUser_522327=eyJpZCI6IjU0MGE3Mjg1LTEwNWYtNTQzYy04ODc3LWJlNWJlMjRiYjUyZiIsImNyZWF0ZWQiOjE3MjU0MTg4MTExODAsImV4aXN0aW5nIjp0cnVlfQ==;"
    "__adm_upl=eyJ0aW1lIjoxNzI1NDIwNzAyLCJfdXBsIjoiNDYzMy0wMTY2ZDdjZDNiMzZjODE5NTBlYWNlYmZmMmVkYTNjZCJ9;"
    "__tb=0;"
    "__IP=1934495598;"
    "__UF=-1;"
    "__uif=__ui%3A-1%7C__create%3A1725418811%7C__uid%3A6054188111182994940;"
    "cto_bundle=1oJWg19TUGZTTUIzeG1GbGdndUp5STkzdnZZSllvYjR0akowTnlWQzZHdUdBVGFKa2J3UklLSWx4cEtWNlVWaHIlMkJFbk8lMkZDY044eG1VWnVtRTVYbmhUU3h3ODRWRXV0NllwV0NjZGpyMVRvMWgwTHRseGUxSElJc01PcCUyQm9CVkxhcWNvTw;"
    "_ga_S9GLR1RQFJ=GS1.1.1725418807.1.1.1725420632.37.0.0;"
    "amp_99d374=MZMTvY0_CsEkvMsEtMRsBc...1i6tfj537.1i6thav2h.1t.2b.48"
}

headers = {
    "User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36 Edg/128.0.0.0",
    "Accept":"application/json, text/plain, */*",
    "Accept-Language":"en-US,en;q=0.9",
    "Referer":"https://tiki.vn/dien-thoai-may-tinh-bang/c1789",
    "X-Guest-Token": "13afeTyco7qZWnRzmIwiUHXB5Y9MVAGN",
    "Connection":"keep-alive",
    "TE":"Trailers"
}   

params={
    "limit": "40",
    "include": "advertisement",
    "aggregations": "2",
    "trackity_id": "8b9792d0-5390-e279-c6c2-bae2ddf893cd",
    "version": "home-personalized",
    "category": "1789",
    "page": "1",
    "src": "c1789",
    "urlKey": "dien-thoai-may-tinh-bang"
}

product_id = []

for index in range(1,21):
    params["page"] = str(index)
    response = requests.get("https://tiki.vn/api/personalish/v1/blocks/listings?", headers=headers, params=params)
    if response.status_code == 200:
        print("request successful")
        data = response.json()
        for item in data["data"]:
            product_id.append(item["id"])
    else:
        print("request failed")
    time.sleep(random.randint(1,2))
    
df = pd.DataFrame(product_id, columns=["product_id"])
df.to_csv("product_id.csv", index=False)
    