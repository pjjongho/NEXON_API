# Baram/api_request/stat/char_stat.py

import os
import pandas as pd
import requests
import time
from tqdm import tqdm

# apy key load
filename = './baram_3.txt'
base_dir = os.path.dirname(__file__)
filepath = os.path.join(base_dir, filename)

with open(filepath, 'r') as file:
    api_key = file.read().strip()

headers = {"x-nxopen-api-key":api_key}

# stat api
def get_stat(ocid):
    try:
        url = f"https://open.api.nexon.com/baram/v1/character/stat?ocid={ocid}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f'[ERROR] {ocid} - {response.status_code} {response.text}')
            return None
    except Exception as e:
        print(f'[EXCEPTION] {ocid} - {e}')
        return None
    
# ocid.csv load
ocid_df = pd.read_csv('./Baram/data/ocid.csv')

# save list
results = []

# retrieveal api
for _, row in tqdm(ocid_df.iterrows(), total=len(ocid_df)):
    ocid = row['ocid']
    character_name = row['character_name']
    server_name = row['server_name']
    job = row['job'] if 'job' in row else None

    try:
        data = get_stat(ocid)
        if data:
            data['ocid'] = ocid
            data['character_name'] = character_name
            data['server_name'] = server_name
            data['job'] = job
            results.append(data)
        time.sleep(1.5)
    except Exception as e:
        print(f'[ERROR] {character_name} ({server_name}) : {e}')
        continue

# 저장
stat_df = pd.DataFrame(results)
stat_df.to_csv('./Baram/data/stat.csv', index=False, encoding='utf-8-sig')
