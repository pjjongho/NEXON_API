import pandas as pd
from tqdm import tqdm
import time
from api_request.char_info.char_info import get_ocid, get_character_info

# 닉네임 불러오기
nickname_df = pd.read_csv('./data/nickname.csv')
nickname_list = nickname_df['nickname'].tolist()

# save result
results = []

for nickname in tqdm(nickname_list):
    try:
        ocid = get_ocid(nickname)
        if ocid is None:
            continue

        info = get_character_info(ocid)
        if info is None:
            continue

        info['nickname'] = nickname
        results.append(info)

        time.sleep(1.5)

    except Exception as e:
        print(f"[ERROR] {nickname} : {e}")

# save dataframe
df = pd.DataFrame(results)
df.to_csv('./data/char_info.csv', index=False, encoding='utf-8-sig')