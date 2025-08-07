# collected_json.py
#
# 닉네임 하나 넣으면 → 관련된 모든 유저 데이터 싹 긁어서 json/csv 저장하고 feature_engineering까지 바로 실행
#
# 동작 순서:
# 1. 입력한 닉네임 + api_key 불러와서 ouid 조회
# 2. 해당 유저의 매치 ID 리스트 가져오기
# 3. 첫 번째 매치의 match-detail 정보 불러오고, 같이 잡힌 유저 닉네임 전부 수집
# 4. 매치에 포함된 모든 유저의 basic/rank/recent/tier 정보 API로 호출
#    - 여기서 ouid도 같이 저장해서 나중에 병합할 때 ID 기준으로 정확하게 맞출 수 있게 함
# 5. 각 유저별 API 호출 결과를 json 파일로 저장
#    - 폴더 구조: collected_data/basic_json, rank_json, recent_json, tier_json
#    - 파일 이름: {수집시각}_{ouid}_{닉네임}_{API코드}.json
# 6. user_name + ouid 매핑 CSV로 저장 (추후 병합이나 디버깅용)
# 7. match-detail JSON과 match ID JSON도 따로 저장
# 8. match-detail 내용을 DataFrame으로 변환해서 df_match.csv로 저장
# 9. feature_engineering 호출해서 df_final.csv까지 만들어줌
#
# 결과적으로 한 번 실행하면:
# - json: 모든 API 호출 결과가 raw 형태로 저장됨
# - csv: df_match, df_merged, df_final, user_summary, match_results 등 가공 데이터 생성


import json
import os
import pandas as pd
from datetime import datetime
from api_request.get_ouid import get_ouid
from api_request.get_basic import get_basic
from api_request.get_rank import get_rank
from api_request.get_recent_info import get_recent_info
from api_request.get_tier import get_tier
from api_request.get_match import get_match
from api_request.get_match_detail import get_match_detail
from utils.feature_engineering import feature_engineering

def collected_api_save_json():
    # 경로 고정 (스크립트 위치 기준)
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "collected_data"))
    analysis_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "analysis"))

    # 1. 닉네임, api_key 입력
    nickname = input("유저 닉네임 입력 : ")
    with open(os.path.join(os.path.dirname(__file__), "..", "api_key.txt")) as f:
        api_key = f.read().strip()

    # 2. ouid 조회 및 match id 호출
    ouid = get_ouid(nickname, api_key)
    if not ouid:
        print(f"[SKIP] 유저 '{nickname}'는 OUID를 못가져옴")
        return

    match_ids = get_match(ouid, api_key)
    if not match_ids:
        print(f"[SKIP] 유저 '{nickname}'의 매치 기록 없음")
        return

    # 3. match-detail info + 같은 매치에 잡힌 유저 닉네임 파싱
    detail, participants_nicknames = get_match_detail(match_ids[0], api_key)

    # 4. user-info 수집
    user_data = []
    for nickname in participants_nicknames:
        ouid_p = get_ouid(nickname, api_key)
        if not ouid_p:
            continue
        try:
            basic = get_basic(ouid_p, api_key)
            basic['ouid'] = ouid_p
            rank = get_rank(ouid_p, api_key)
            recent = get_recent_info(ouid_p, api_key)
            tier = get_tier(ouid_p, api_key)
            user_data.append({
                "ouid": ouid_p,
                "user_name": basic.get("user_name", nickname),
                "basic": basic,
                "rank": rank,
                "recent": recent,
                "tier": tier
            })
        except Exception as e:
            print(f"[ERROR] {nickname} 정보 조회 에러: {e}")

    # 5. json 저장
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    api_codes = {
        "basic": "bs",
        "rank": "rk",
        "recent": "ri",
        "tier": "tr",
        "match": "mc",
        "match_detail": "md"
    }
    for folder in ["basic_json", "rank_json", "recent_json", "tier_json", "match_json", "match-detail_json"]:
        os.makedirs(os.path.join(base_dir, folder), exist_ok=True)

    for user in user_data:
        for key, code in [("basic", "bs"), ("rank", "rk"), ("recent", "ri"), ("tier", "tr")]:
            file_path = os.path.join(base_dir, f"{key}_json", f"{timestamp}_{user['ouid']}_{user['user_name']}_{code}.json")
            with open(file_path, "w", encoding='utf-8') as f:
                json.dump(user[key], f, indent=2, ensure_ascii=False)

    # 6. user_name + ouid 호출 횟수 통계 저장
    summary_path = os.path.join(base_dir, "user_requests_summary.csv")
    df_map = pd.DataFrame([{"ouid": u["ouid"], "user_name": u["user_name"]} for u in user_data])

    if os.path.exists(summary_path):
        df_old = pd.read_csv(summary_path)
        df_all = pd.concat([df_old, df_map], ignore_index=True)
    else:
        df_all = df_map.copy()

    df_summary = (
        df_all
        .groupby(["ouid", "user_name"], as_index=False)
        .size()
        .rename(columns={"size": "call_count"})
    )

    df_summary.to_csv(summary_path, index=False, encoding="utf-8-sig")

    # 7. match-detail-info 저장
    match_detail_path = os.path.join(base_dir, "match-detail_json", f"{timestamp}{api_codes['match_detail']}.json")
    with open(match_detail_path, "w", encoding='utf-8') as f:
        json.dump(detail, f, indent=2, ensure_ascii=False)

    # 8. match-id 저장
    match_path = os.path.join(base_dir, "match_json", f"{timestamp}{api_codes['match']}.json")
    with open(match_path, "w", encoding='utf-8') as f:
        json.dump({"match_id": match_ids}, f, indent=2, ensure_ascii=False)

    # 9. match-detail.csv 저장
    os.makedirs(analysis_dir, exist_ok=True)
    match_detail_df = pd.DataFrame(detail["match_detail"])
    match_detail_df["match_id"] = detail["match_id"]
    match_detail_df["match_type"] = detail["match_type"]
    match_detail_df["match_mode"] = detail["match_mode"]
    match_detail_df["match_map"] = detail["match_map"]
    match_detail_df["date_match"] = detail["date_match"]
    match_detail_df.to_csv(os.path.join(analysis_dir, "df_match.csv"), index=False, encoding="utf-8-sig")

    # 10. feature_engineering 실행
    df = feature_engineering(
        match_path=match_detail_path,
        save_path=os.path.join(analysis_dir, "df_final.csv")
    )

    return df