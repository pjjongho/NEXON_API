# ouid.csv를 통해 유저 랭크 정보 수집
# {
#   "user_name": "string",
#   "grade": "string",
#   "grade_exp": 0,
#   "grade_ranking": 0,
#   "season_grade": "string",
#   "season_grade_exp": 0,
#   "season_grade_ranking": 0
# }

import pandas as pd
import requests
import time
from tqdm import tqdm

with open('./SA/api_request/rank/sa_4.txt','r') as f:
    api_key = f.read().strip()

# ouid.csv load
df = pd.read_csv('./SA/collected_data/ouid.csv')
ouids = df['ouid'].dropna().tolist()

results = []
for ouid in tqdm(ouids):
    try:
        url = f"https://open.api.nexon.com/suddenattack/v1/user/rank?ouid={ouid}"
        response = requests.get(
            url,
            headers={"x-nxopen-api-key" : api_key}
        )

        if response.status_code == 200:
            data = response.json()
            data['ouid'] = ouid # ouid가 식별자 임 즉 다른 데이터와 조인하려면 ouid를 써야하기 때문에 무조건 넣어줘야함
            results.append(data)
        else:
            print(f'{ouid} - {response.status_code} - {response.text}')

        time.sleep(1.0)
    
    except Exception as e:
        print(f'[EXCEPTION] {ouid} - {e}')
        time.sleep(1.0)

pd.DataFrame(results).to_csv('./SA/collected_data/rank_info.csv', index=False, encoding='utf-8-sig')
        