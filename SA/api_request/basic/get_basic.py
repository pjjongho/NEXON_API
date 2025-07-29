# get_ouid.py를 통해 수집된 data/ouid.csv를 통해서
# 캐릭터의 basic 정보를 수집

import pandas as pd
import requests
import time
from tqdm import tqdm

with open('api 파일이 있는 경로', 'r') as f:
    api_key=f.read().strip()

# ouid.csv load
df = pd.read_csv('./SA/data/ouid.csv')
ouids = df['ouid'].dropna().tolist()

results = []

for ouid in tqdm(ouids):
    try:
        url = f"https://open.api.nexon.com/suddenattack/v1/user/basic?ouid={ouid}"
        response = requests.get(
            url,
            headers={"x-nxopen-api-key":api_key}
        )

        if response.status_code == 200:
            data = response.json()
            data["ouid"] = ouid # 나중에 병합을 위해 ouid 포함
            results.append(data)
        else:
            print(f"{ouid} - {response.status_code} - {response.text}")

        time.sleep(1.0)
    
    except Exception as e:
        print(f"[EXCEPTION] {ouid} - {e}")
        time.sleep(1.0)

pd.DataFrame(results).to_csv('./SA/data/basic.csv', index=False, encoding='utf-8-sig')