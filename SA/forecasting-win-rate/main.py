import json
import os
import pandas as pd
from api_request.get_ouid import get_ouid
from api_request.get_basic import get_basic
from api_request.get_rank import get_rank
from api_request.get_recent_info import get_recent_info
from api_request.get_tier import get_tier
from api_request.get_match import get_match
from api_request.get_match_detail import get_match_detail
from utils.feature_engineering import feature_engineering

# 1. nickname과 api_key 입력
nickname = input("검색할 닉네임을 입력하세요: ")
with open("api_key.txt") as f:
    api_key = f.read().strip()

# 2. 유저 OUID 조회 및 매치 ID 가져오기
ouid = get_ouid(nickname, api_key)
match_ids = get_match(ouid, api_key)

# 3. 첫 번째 매치 상세 정보 가져오기 + 함께한 유저 닉네임 파싱
detail, participants_nicknames = get_match_detail(match_ids[0], api_key)

# 4. 유저들 정보 수집
user_data = []
for nickname in participants_nicknames:
    ouid = get_ouid(nickname, api_key)
    if not ouid:
        continue  # ouid 못 찾은 경우 스킵

    try:
        basic = get_basic(ouid, api_key)
        rank = get_rank(ouid, api_key)
        recent = get_recent_info(ouid, api_key)
        tier = get_tier(ouid, api_key)
        user_data.append({
            "ouid": ouid,
            "basic": basic,
            "rank": rank,
            "recent": recent,
            "tier": tier
        })
    except Exception as e:
        print(f"[SKIP] 유저 '{nickname}'의 세부 정보 수집 중 오류 발생: {e}")

# 5. JSON 저장
os.makedirs("./collected_data", exist_ok=True)
for user in user_data:
    ouid = user["ouid"]
    for key in ["basic", "rank", "recent", "tier"]:
        with open(f"./collected_data/{ouid}_{key}.json", "w", encoding="utf-8") as f:
            json.dump(user[key], f, indent=2, ensure_ascii=False)

# 6. 매치 상세 정보도 저장 (JSON + CSV)
with open(f"./collected_data/match_detail.json", "w", encoding="utf-8") as f:
    json.dump(detail, f, indent=2, ensure_ascii=False)

# 7. match_detail.csv 저장
os.makedirs("./analysis", exist_ok=True)

match_detail_df = pd.DataFrame(detail["match_detail"])
match_detail_df["match_id"] = detail["match_id"]
match_detail_df["match_type"] = detail["match_type"]
match_detail_df["match_mode"] = detail["match_mode"]
match_detail_df["match_map"] = detail["match_map"]
match_detail_df["date_match"] = detail["date_match"]

match_detail_df.to_csv("./analysis/df_match.csv", index=False, encoding="utf-8-sig")

df = feature_engineering(
    match_path="./collected_data/match_detail.json",
    merged_path="./analysis/df_merged.csv",
    save_path="./analysis/df_final.csv"
)

print(df.head())
