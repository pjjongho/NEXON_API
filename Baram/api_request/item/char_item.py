# 데이터 분석을 진행하던 도중 캐릭터 별로 장착된 아이템의 스탯을 확인하기 위해 진행
#

import os
import pandas as pd
import requests
from tqdm import tqdm

filename = './baram_2.txt'
base_dir = os.path.dirname(__file__)
filepath = os.path.join(base_dir, filename)

with open(filepath, 'r') as file:
    api_key = file.read().strip()

headers = {"x-nxopen-api-key" : api_key}

# 데이터는 ./Baram/main_analysis/merged.csv에서 활용
df = pd.read_csv('./Baram/main_analysis/data/merged_df.csv')

# api 호출
def get_item(ocid):
    url = f"https://open.api.nexon.com/baram/v1/character/item-equipment?ocid={ocid}"
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get('item_equipment', [])
        else:
            print(f'[ERROR] {ocid} - {response.status_code}')
            return None
    except Exception as e:
        print(f'[EXCEPTION] {ocid} - {e}')
        return None


results = []
for ocid in tqdm(df['ocid'].unique()):
    item_data = get_item(ocid)
    if item_data is not None:
        for item in item_data:
            item['ocid'] = ocid
            results.append(item)

item_df = pd.DataFrame(results)
item_df.to_csv('./Baram/data/item_df.csv', index=False, encoding='utf-8-sig')