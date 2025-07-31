# ouid.csv의 ouid를 통해
# 유저의 매치 정보 조회
# 매치 정보는 각 모드와 타입이 존재함
# 따라서 전부 수집하기엔 시간적인 문제와 호출량에 대한 문제가 발생하므로
# 모드는 개인전, 폭파미션 2개 
# 타입은 솔로랭크, 클랜랭크, 퀵매치 클랜, 랭크전 파티, 일반 5개
# 총 4개의 유형에 대해서 수집
# api_key = sa_4.txt

# {
#   "match": [
#     {
#       "match_id": "string",
#       "match_type": "string",
#       "match_mode": "string",
#       "date_match": "2023-12-14T08:28:35Z",
#       "match_result": "string",
#       "kill": 0,
#       "death": 0,
#       "assist": 0
#     }
#   ]
# }

import pandas as pd
import requests
import time
from tqdm import tqdm

with open('./SA/api_request/match/sa_3.txt','r') as f:
    api_key = f.read().strip()

results = []

# ouid load
df = pd.read_csv('./SA/collected_data/ouid.csv')
ouids = df['ouid'].dropna().tolist()

# 모든 모드 및 타입 정의
match_modes = ["폭파미션"] # 개인전, 데스매치, 폭파미션
match_types = ["퀵매치 클랜전"] # 일반전, 클랜전, 퀵매치 클랜전, 클랜 랭크전, 랭크전 솔로, 랭크전 파티, 토너먼트


for ouid in tqdm(ouids):
    for mode in match_modes:
        for mtype in match_types:
            try:
                url = f"https://open.api.nexon.com/suddenattack/v1/match?ouid={ouid}&match_mode={mode.strip()}&match_type={mtype.strip()}"
                
                response = requests.get(
                    url, 
                    headers={"x-nxopen-api-key": api_key}
                    )
                
                if response.status_code == 200:
                    data = response.json()
                    data['ouid'] = ouid
                    results.append(data)
                else:
                    print(f'{ouid} - {response.status_code} - {response.text}')
                time.sleep(0.5)

            except Exception as e:
                print(f'[EXCEPTION] {ouid} - {e}')
                time.sleep(0.5)

# 저장할 데이터 이름
# match-normal-individual - v
# match-solo-rank - v
# match-clan-rank - v
# match-quick-clan - v
# match-rank-party


pd.DataFrame(results).to_csv('./SA/collected_data/match-quick-clan.csv', index=False, encoding='utf-8-sig')
