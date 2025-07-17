from crawler.nickname_crawler import get_top_nicknames
from api_request.char_info import *
import pandas as pd
from tqdm import tqdm
import time

if __name__ == "__main__":

    # 1. 닉네임 수집
    names = get_top_nicknames(500)
    df = pd.DataFrame(names, columns=["nickname"])
    print(f"{len(names)}'s collect complete")
    df.to_csv("./nicknames.csv", index=False, encoding="utf-8-sig")

    # 2. 캐릭터 정보 수집
    nickname_list = df['nickname'].dropna().unique().tolist()

    results = []
    fail_list = []

    for nickname in tqdm(nickname_list):
        ocid = get_ocid(nickname)
        if ocid:

            info = get_character_info(ocid) # 캐릭터 정보
            popularity_info = get_popularity(ocid) # 인기도
            character_stat = get_character_stat(ocid) # 스탯
            character_ability_info = get_character_ability(ocid) # 어빌리티
            dojang_info = get_dojang(ocid) # 무릉도장

            if info:
                results.append({
                    "nickname" : nickname,
                    "character_name": info["character_name"],
                    "character_level": info["character_level"],
                    "character_class" : info["character_class"],
                    "world_name":info["world_name"],
                    "character_gender":info["character_gender"],
                    "character_class_level":info["character_class_level"],
                    "character_popularity" : popularity_info["popularity"] if popularity_info else None,
                    "character_stat": character_stat if character_stat else None,
                    "ability_grade": character_ability_info["ability_grade"] if character_ability_info else None,
                    "ability_info_1" : character_ability_info["ability_info"][0] if character_ability_info else None,
                    "ability_info_2" : character_ability_info["ability_info"][1] if character_ability_info else None,
                    "ability_info_3" : character_ability_info["ability_info"][2] if character_ability_info else None,
                    "dojang_best_time" : dojang_info["dojang_best_time"] if dojang_info else None,
                    "dojang_best_floor" : dojang_info["dojang_best_floor"] if dojang_info else None

                })
            else:
                fail_list.append(nickname)
        else:
            fail_list.append(nickname)
        time.sleep(1.5)

# 데이터 프레임 변환
pd.DataFrame(results).to_csv('./character_info.csv', index=False, encoding='utf-8-sig')

# 조회 안된 캐릭터들
pd.Series(fail_list).to_csv('./fail_list.csv',index=False, encoding='utf-8-sig')