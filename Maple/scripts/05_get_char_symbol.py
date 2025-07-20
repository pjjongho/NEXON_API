import pandas as pd
from tqdm import tqdm
import time
from api_request.char_info.char_info import get_ocid
from api_request.symbol.symbol import get_character_symbol

# 닉네임 불러오기
nickname_df = pd.read_csv('./data/nickname.csv')
nickname_list = nickname_df['nickname'].tolist()

results = []

for nickname in tqdm(nickname_list):
    try:
        ocid = get_ocid(nickname)
        if ocid is None:
            continue

        symbol = get_character_symbol(ocid)
        if symbol is None:
            continue

        symbol['nickname'] = nickname
        results.append(symbol)

        time.sleep(1.5)

    except Exception as e:
        print(f"[ERROR] {nickname} : {e}")

# save dataframe
df = pd.DataFrame(results)
df.to_csv('./data/symbol_info.csv', index=False, encoding='utf-8-sig')