from crawler.nickname_crawler import get_top_nicknames
from api_request.char_info import get_ocid, get_character_info
from api_request.popularity import get_popularity
from api_request.stat import get_character_stat
from api_request.ability import get_character_ability
from api_request.dojang import get_dojang

import pandas as pd
from tqdm import tqdm
import time
import os

if __name__ == "__main__":

    # 1. 닉네임 수집
    names = get_top_nicknames(500)
    nickname_df = pd.DataFrame(names, columns=['nickname'])
    nickname_df.to_csv("./data/nickname.csv", index=False, encoding='utf-8-sig')
    print(f"{len(names)} nicknames collected")

    nickname_list = nickname_df['nickname'].dropna().unique().tolist()

    # 각 api 리스트 초기화
    char_info_list = [] # 캐릭정보
    dojang_list = [] # 무릉도장
    popularity_list = [] # 인기도
    stat_list = [] # 스탯
    ability_list = [] # 어빌리티
    fail_list = [] # 호출되지 못한 캐릭터들 모아두기

    for nickname in tqdm(nickname_list):
        try:
            ocid = get_ocid(nickname)
            if not ocid:
                fail_list.append((nickname, "ocid 조회 실패함"))
                continue

            # 이제 각 api 호출
            char_info = get_character_info(ocid)
            popularity = get_popularity(ocid)
            stat = get_character_stat(ocid)
            ability = get_character_ability(ocid)
            dojang = get_dojang(ocid)

            # char_info 저장
            if char_info:
                char_info_list.append({
                    "nickname" : nickname, **{k: v for k, v in char_info.items()}})

            # 무릉도장
            if dojang:
                dojang_list.append({
                    "nickname":nickname,
                    "dojang_best_floor":dojang.get("dojang_best_floor"),
                    "dojang_best_time" : dojang.get("dojang_best_time")
                })
            
            # 인기도
            if popularity:
                popularity_list.append({
                    "nickname" : nickname,
                    "popularity" : popularity.get("popularity")
                })

            # 스탯
            """
            스탯은 final_stat : [{

            'stat_name':'최소스탯공격력', 
            'stat_value':float

             }] 형식으로 저장되어 있어서 for 문을 통해 stat_name, stat_value를 가져옴
             """
            if stat and "final_stat" in stat:
                stat_row = {"nickname":nickname}
                for item in stat["final_stat"]:
                    stat_row[item["stat_name"]] = item["stat_value"]
                stat_list.append(stat_row)

            # 어빌리티
            """
            어빌리티는 총 세개의 항목이 존재함 그 항목에 맞게 api를 호출 받을 수 있도록 구성
           """

            if ability:
                row = {
                    "nickname" : nickname,
                    "ability_grade" : ability.get("ability_grade")
                }
                ability_infos = ability.get("ability_info", [])

                for i in range(3):
                    row[f"ability_info_{i+1}"] = ability_infos[i] if i < len(ability_infos) else None
                ability_list.append(row)

        except Exception as e:
            fail_list.append((nickname, str(e)))

        time.sleep(1.5)

    # csv 파일 저장
    pd.DataFrame(char_info_list).to_csv('./data/char_info.csv', index=False, encoding='utf-8-sig')
    pd.DataFrame(dojang_list).to_csv('./data/dojang.csv',index=False, encoding='utf-8-sig')
    pd.DataFrame(popularity_list).to_csv('./data/popularity.csv',index=False, encoding='utf-8-sig')
    pd.DataFrame(stat_list).to_csv('./data/stat.csv',index=False, encoding='utf-8-sig')
    pd.DataFrame(fail_list).to_csv('./data/fail_list.csv',index=False, encoding='utf-8-sig')
    pd.DataFrame(ability_list).to_csv('./data/ability.csv', index=False, encoding='utf-8-sig')