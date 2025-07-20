import warnings
warnings.filterwarnings(action='ignore')

import os
import requests
import pandas

# api 호출
filename = 'symbol_api.txt'
base_dir = os.path.dirname(__file__)
filepath = os.path.join(base_dir, filename)

with open(filepath, 'r') as file:
    api_key = file.read().strip()

headers = {"x-nxopen-api-key" : api_key}

# character symbol information
def get_character_symbol(ocid):
    url = f"https://open.api.nexon.com/maplestory/v1/character/symbol-equipment?ocid={ocid}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print("심볼 조회 실패 : ", response.status_code, response.text)
        return None