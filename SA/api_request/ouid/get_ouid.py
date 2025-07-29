# 계정 식별자 조회
# 닉네임을 크롤링 하여 수집한 nickname.csv를 통해 ouid 조회

import pandas as pd
import requests
import time
from tqdm import tqdm
from urllib.parse import quote

# API 키 불러오기
with open('api 파일이 있는 경로', 'r') as f:
    api_key = f.read().strip()

# 닉네임 CSV 불러오기
nickname_df = pd.read_csv('./crwaler/nickname.csv')
nicknames = nickname_df['nickname'].dropna().tolist()

results = []

# ouid 수집
for nickname in tqdm(nicknames):
    try:
        # 닉네임 URL 인코딩
        encoded_nickname = quote(nickname)

        # API 요청
        response = requests.get(
            url=f"https://open.api.nexon.com/suddenattack/v1/id?user_name={encoded_nickname}",
            headers={"x-nxopen-api-key": api_key}
        )

        if response.status_code == 200:
            data = response.json()
            ouid = data.get('ouid')
            if ouid:
                results.append({
                    "user_name": nickname,
                    "ouid": ouid
                })
            else:
                print(f'[ERROR] {nickname} {response.status_code} → ouid 없음')
        else:
            print(f'[ERROR] {nickname} {response.status_code} {response.text}')
    except Exception as e:
        print(f'[EXCEPTION] {nickname}: {e}')

    time.sleep(1.0)

# 결과 저장
pd.DataFrame(results).to_csv('./data/ouid.csv', index=False, encoding='utf-8-sig')
print(f'총 {len(results)}개의 ouid 수집')
