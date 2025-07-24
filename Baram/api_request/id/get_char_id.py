# get_id.py

import pandas as pd
import time
from tqdm import tqdm
from Baram.api_request.id.char_id import get_id

# 서버 이름 정제 함수
def clean_server_name(raw_server):
    valid_servers = ['연', '무휼', '유리', '하자', '호동', '진']
    for valid in valid_servers:
        if valid in raw_server:
            return valid
    return raw_server.strip()  # 혹시라도 못 찾으면 공백 제거 후 그대로 반환

# 닉네임 + 서버 조합 불러오기
df = pd.read_csv('./Baram/data/baram_ranker.csv')

# 중복 제거
nickname_server_list = df[['게임아이디', '서버']].drop_duplicates().values.tolist()

result = []

for nickname, server in tqdm(nickname_server_list):
    try:
        cleaned_server = clean_server_name(server)
        ocid = get_id(nickname, cleaned_server)

        if ocid is None:
            continue

        result.append({
            'nickname': nickname,
            'server': cleaned_server,
            'ocid': ocid
        })

        time.sleep(1.5)  # 호출 제한 대비
    except Exception as e:
        print(f'[ERROR] {nickname} ({server}) : {e}')

# 저장
pd.DataFrame(result).to_csv('./Baram/data/ocid.csv', index=False, encoding='utf-8-sig')
