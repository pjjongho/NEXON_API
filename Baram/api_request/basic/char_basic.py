# Baram/api_request/basic/char_basic.py

import os
import pandas as pd
import requests
import time
from tqdm import tqdm

# API 키 불러오기
filename = './baram_2.txt'
base_dir = os.path.dirname(__file__)
filepath = os.path.join(base_dir, filename)

with open(filepath, 'r') as file:
    api_key = file.read().strip()

headers = {"x-nxopen-api-key": api_key}

# Basic API 호출 함수
def get_basic(ocid):
    try:
        url = f"https://open.api.nexon.com/baram/v1/character/basic?ocid={ocid}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f'[ERROR] {ocid} - {response.status_code} {response.text}')
            return None
    except Exception as e:
        print(f'[EXCEPTION] {ocid} - {e}')
        return None

# ocid.csv 불러오기
ocid_df = pd.read_csv('./Baram/data/ocid.csv')

# 결과 저장용 리스트
results = []

# API 호출 반복
for _, row in tqdm(ocid_df.iterrows(), total=len(ocid_df)):
    ocid = row['ocid']
    character_name = row['character_name']
    server_name = row['server_name']
    job = row['job'] if 'job' in row else None

    try:
        data = get_basic(ocid)
        if data:
            data['character_name'] = character_name
            data['server_name'] = server_name
            data['job'] = job
            results.append(data)
        time.sleep(1.2)  # 호출 제한 방지
    except Exception as e:
        print(f'[ERROR] {character_name} ({server_name}) : {e}')
        continue

# 저장
basic_df = pd.DataFrame(results)
basic_df.to_csv('./Baram/data/basic.csv', index=False, encoding='utf-8-sig')
