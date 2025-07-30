# get_ouid.py를 통해 수집된 data/ouid.csv를 통해
# 캐릭터의 티어 정보 수집
# {
#   "user_name": "string",
#   "solo_rank_match_tier": 0,
#   "solo_rank_match_score": 0,
#   "party_rank_match_tier": 0,
#   "party_rank_match_score": 0
# }

import pandas as pd
import requests
import time
from tqdm import tqdm

with open('./SA/api_request/tier/sa_2.txt', 'r') as f:
    api_key = f.read().strip()

# ouid.csv load
df = pd.read_csv('./SA/collected_data/ouid.csv')
ouids = df['ouid'].dropna().tolist()

results = []

for ouid in tqdm(ouids):
    try:
        url = f"https://open.api.nexon.com/suddenattack/v1/user/tier?ouid={ouid}"
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

pd.DataFrame(results).to_csv('./SA/collected_data/tier_info.csv', index=False, encoding='utf-8-sig')
