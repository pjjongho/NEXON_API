# get_ouid.py를 통해 수집된 collected_data/ouid.csv를 통해
# 유저의 최근 동향 recent-info 수집
# api_key = sa_1.txt

# {
#   "user_name": "string",
#   "recent_win_rate": 0,
#   "recent_kill_death_rate": 0,
#   "recent_assault_rate": 0,
#   "recent_sniper_rate": 0,
#   "recent_special_rate": 0
# }

import pandas as pd
import requests
import time
from tqdm import tqdm

with open('./SA/api_request/recent-info/sa_3.txt', 'r') as f:
    api_key = f.read().strip()

# ouid.csv load
df = pd.read_csv('./SA/collected_data/ouid.csv')
ouids = df['ouid'].dropna().tolist()

results = []

for ouid in tqdm(ouids):
    try:
        url = f"https://open.api.nexon.com/suddenattack/v1/user/recent-info?ouid={ouid}"
        response = requests.get(
            url,
            headers={"x-nxopen-api-key":api_key}
        )

        if response.status_code == 200:
            data = response.json()
            data['ouid'] = ouid
            results.append(data)
        else:
            print(f'{ouid} - {response.status_code} - {response.text}')

        time.sleep(1.0)

    except Exception as e:
        print(f'[EXCEPTION] {ouid} - {e}')
        time.sleep(1.0)

pd.DataFrame(results).to_csv('./SA/collected_data/recent-info.csv', index=False, encoding='utf-8-sig')
