import os
import requests
import pandas as pd
from tqdm import tqdm
from urllib.parse import quote
import time

# API key load
filename = './baram_1.txt'
base_dir = os.path.dirname(__file__)
filepath = os.path.join(base_dir, filename)

with open(filepath, 'r') as file:
    api_key = file.read().strip()

headers = {"x-nxopen-api-key": api_key}

# ocid 조회
def get_id(character_name, server_name):
    try:
        encoded_name = quote(character_name)
        encoded_server = quote(server_name)
        url = f"https://open.api.nexon.com/baram/v1/id?character_name={encoded_name}&server_name={encoded_server}"

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get("ocid")
        else:
            print(f'{character_name} ({server_name}) - {response.status_code} {response.text}')
            return None
    except Exception as e:
        print(f'{character_name} ({server_name}) - {e}')
        return None

# 크롤링한 랭커 CSV에서 캐릭터명 + 서버 + 직업 추출
df = pd.read_csv('./Baram/data/baram_ranker.csv')
df = df[['게임아이디', '서버', '직업']].drop_duplicates()

results = []
for _, row in tqdm(df.iterrows(), total=len(df)):
    nickname = row['게임아이디']
    server = row['서버']
    job = row['직업']

    ocid = get_id(nickname, server)
    if ocid:
        results.append({
            'character_name': nickname,
            'server_name': server,
            'job': job,
            'ocid': ocid
        })
        time.sleep(1.5)

# 저장
pd.DataFrame(results).to_csv('./Baram/data/ocid.csv', index=False, encoding='utf-8-sig')
