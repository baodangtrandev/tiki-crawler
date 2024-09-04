import requests
import time
import random
import pandas as pd
from tqdm import tqdm

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
    "Referer":"https://tiki.vn/dien-thoai-samsung-galazy-a15-lte-8gb-128gb-da-kich-hoat-bao-hanh-dien-tu-hang-chinh-hang-p273951550.html?",
    "X-Guest-Token": "13afeTyco7qZWnRzmIwiUHXB5Y9MVAGN",
    "Connection":"keep-alive",
    "TE":"Trailers"
}   

params={
    "platform":"web",
    "spid":"273952409",
    "version":"3"
}

def crawler_product_info(json_data):
    d = dict()
    d['id'] = json_data['id']
    d['sku'] = json_data['sku']
    d['prodcut_name'] = json_data['name']
    d['short_description'] = json_data['short_description']
    d['price'] = json_data['price']
    d['list_price'] = json_data['list_price']
    if json_data.get('tracking_info') is not None:
        if 'amplitude' in json_data['tracking_info']:
            amplitude_info = json_data['tracking_info']['amplitude']
            
            d['is_authentic'] = amplitude_info.get('is_authentic', None)
            d['is_freeship_xtra'] = amplitude_info.get('is_freeship_xtra', None)
            d['is_hero'] = amplitude_info.get('is_hero', None)
    else:
        d['is_authentic'] = d['is_freeship_xtra'] = d['is_hero'] = None
    d['discount'] = json_data['discount']
    d['discount_rate'] = json_data['discount_rate']
    d['rating_average'] = json_data['rating_average']
    d['review_count'] = json_data['review_count']
    d['favourite_count'] = json_data['favourite_count']
    d['inventory_status'] = json_data['inventory_status']
    d['inventory_status'] = json_data['inventory_status']
    if 'all_time_quantity_sold' in json_data:
        d['sold_count'] = json_data['all_time_quantity_sold'] if json_data['all_time_quantity_sold'] is not None else 0
    elif 'quantity_sold' in json_data:
        d['sold_count'] = json_data['quantity_sold']['value'] if json_data['quantity_sold'] is not None else 0
    else:
        d['sold_count'] = None
    if 'categories' in json_data:
        d['category_id'] = json_data['categories']['id']
        d['category_name'] = json_data['categories']['name']
    d['brand_id'] = json_data['brand']['id']
    d['brand_name'] = json_data['brand']['name']
    #print(json_data['specifications'])
    for specify in json_data['specifications']:
        if specify['name'] == 'Content':
            for content in specify['attributes']:
                if content['code'] == 'battery_capacity':
                    d['battery_capacity'] = content['value']
                if content['code'] == 'brand_country':
                    d['brand_country'] = content['value']
                if content['code'] == 'cpu_speed':
                    d['cpu_speed'] = content['value']
                if content['code'] == 'ho_tro_5g':
                    d['has_5g'] = content['value']
                if content['code'] == 'khe_sim':
                    d['sim_slot'] = content['value']
                if content['code'] == 'product_weight':
                    d['product_weight'] = content['value']
                if content['code'] == 'ram':
                    d['ram'] = content['value']
                if content['code'] == 'rom':
                    d['rom'] = content['value']

    # Ensure missing fields are set to a default value if not found
    d['battery_capacity'] = d.get('battery_capacity', 'NULL')
    d['brand_country'] = d.get('brand_country', 'NULL')
    d['cpu_speed'] = d.get('cpu_speed', 'NULL')
    d['has_5g'] = d.get('has_5g', 'Không')
    d['sim_slot'] = d.get('sim_slot', 'NULL')
    d['product_weight'] = d.get('product_weight', 'NULL')
    d['ram'] = d.get('ram', 'NULL')
    d['rom'] = d.get('rom', 'NULL')
    d['number_options'] = len(json_data['configurable_products']) if 'configurable_products' in json_data else None
    if 'warranty_info' in json_data and json_data['warranty_info'] is not None:
        for warranty in json_data['warranty_info']:
            if warranty['name'] == 'Thời gian bảo hành':
                d['warranty_time'] = warranty['value']
            if warranty['name'] == 'Hình thức bảo hành':
                d['warranty_type'] = warranty['value']
            if warranty['name'] == 'Nơi bảo hành':
                d['warranty_place'] = warranty['value']

    d['warranty_time'] = d.get('warranty_time', 'NULL')
    d['warranty_type'] = d.get('warranty_type', 'NULL')
    d['warranty_place'] = d.get('warranty_place', 'NULL')

    if 'return_policy' in json_data and json_data['return_policy'] is not None:
        d['return_policy'] = json_data['return_policy']['title']
    else:
        d['return_policy'] = "NULL"
    return d

df_id = pd.read_csv("product_id.csv")
product_ids = df_id["product_id"].tolist()
# print(product_ids)

product_infos = []

for pid in tqdm(product_ids):
    response = requests.get(f"https://tiki.vn/api/v2/products/{pid}", headers=headers, params=params)
    if response.status_code == 200:
        print(" request successful")
        data = response.json()
        product_info = crawler_product_info(data)
        product_infos.append(product_info)
    else:
        print(" request failed")
    time.sleep(random.randint(0,1))

df = pd.DataFrame(product_infos)
df.to_csv("product_info.csv", index=False)