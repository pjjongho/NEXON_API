# feature_engineering.py
#
# match-detail JSON과 collected_data 폴더에 저장된 유저 정보 JSON들을 합쳐서
# 학습에 쓸 수 있는 형태의 CSV 파일로 만드는 작업을 함.
#
# 1. match-detail JSON을 불러와서 메타데이터(매치 ID, 타입, 모드, 맵, 날짜) 붙임
# 2. 유저별 경기 결과 집계해서 user_summary 생성 (승/무/패, 킬/데스/어시, 승률, KDA 등)
# 3. user_summary를 user_summary.csv로 따로 저장하는데, 기존 파일이 있으면 새 데이터만 추가하고 중복 제거
# 4. collected_data/basic_json, rank_json, recent_json, tier_json에 있는 파일 읽어서 병합
# 5. df_final.csv를 만들 때는 모델 누설 위험 있는 컬럼(kill_per_match, death_per_match, user_kda 등)은 제외
# 6. df_match.csv, df_merged.csv, df_final.csv, match_results.csv 전부 기존 파일이 있으면 누적 저장

import os
import json
import pandas as pd

def feature_engineering(match_path, save_path):
    # 분석 폴더 절대경로 고정
    analysis_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "analysis"))
    os.makedirs(analysis_dir, exist_ok=True)

    # 1. match_detail 로드
    with open(match_path, 'r', encoding='utf-8') as f:
        match_detail = json.load(f)

    # 루트 메타데이터 추가
    root_match_id = match_detail.get('match_id')
    root_match_type = match_detail.get('match_type')
    root_match_mode = match_detail.get('match_mode')
    root_match_map = match_detail.get('match_map')
    root_date_match = match_detail.get('date_match')

    for player in match_detail['match_detail']:
        player['match_id'] = root_match_id
        player['match_type'] = root_match_type
        player['match_mode'] = root_match_mode
        player['match_map'] = root_match_map
        player['date_match'] = root_date_match

    # 2. DataFrame 변환
    df_match = pd.DataFrame(match_detail['match_detail'])
    df_match['match_result'] = df_match['match_result'].astype(int)

    # 3. 승/무/패 여부 컬럼 (무승부는 0으로 기록)
    df_match['is_win'] = df_match['match_result'].apply(lambda x: 1 if x == 1 else 0)
    df_match['is_draw'] = df_match['match_result'].apply(lambda x: 1 if x == 3 else 0)
    df_match['is_loss'] = df_match['match_result'].apply(lambda x: 1 if x == 2 else 0)

    # 4. 유저별 매치 통계
    user_summary = (
        df_match.groupby('user_name')[['is_win', 'is_draw', 'is_loss', 'kill', 'death', 'assist']]
        .sum()
        .reset_index()
    )
    user_summary['total_matches'] = user_summary[['is_win', 'is_draw', 'is_loss']].sum(axis=1)
    user_summary['actual_win_rate'] = user_summary['is_win'] / user_summary['total_matches']
    user_summary['user_kda'] = (user_summary['kill'] + user_summary['assist']) / user_summary['death'].replace(0, 1)
    user_summary['user_kill'] = user_summary['kill']
    user_summary['user_death'] = user_summary['death']
    user_summary['user_assist'] = user_summary['assist']
    user_summary['kill_per_match'] = user_summary['kill'] / user_summary['total_matches']
    user_summary['death_per_match'] = user_summary['death'] / user_summary['total_matches']
    user_summary['assist_per_match'] = user_summary['assist'] / user_summary['total_matches']

    # match_id 없으면 채우기
    if 'match_id' not in user_summary.columns:
        user_summary['match_id'] = root_match_id

    # 4-1. user_summary.csv 누적 저장
    summary_path = os.path.join(analysis_dir, "user_summary.csv")
    if os.path.exists(summary_path):
        old_summary = pd.read_csv(summary_path)
        # match_id 없으면 빈 컬럼 추가
        if 'match_id' not in old_summary.columns:
            old_summary['match_id'] = None
        user_summary = pd.concat([old_summary, user_summary], ignore_index=True)
        user_summary.drop_duplicates(subset=["user_name", "match_id"], keep="last", inplace=True)
    user_summary.to_csv(summary_path, index=False, encoding="utf-8-sig")

    # 5. collected_data JSON 로드 및 병합
    records = []
    for filename in os.listdir("./collected_data/basic_json"):
        if filename.endswith(".json"):
            try:
                with open(os.path.join("./collected_data/basic_json", filename), encoding='utf-8') as f1, \
                     open(os.path.join("./collected_data/rank_json", filename.replace("bs", "rk")), encoding='utf-8') as f2, \
                     open(os.path.join("./collected_data/recent_json", filename.replace("bs", "ri")), encoding='utf-8') as f3, \
                     open(os.path.join("./collected_data/tier_json", filename.replace("bs", "tr")), encoding='utf-8') as f4:
                    basic = json.load(f1)
                    rank = json.load(f2)
                    recent = json.load(f3)
                    tier = json.load(f4)

                    record = {
                        'user_name': basic.get('user_name', None),
                        'grade_ranking': rank['grade_ranking'],
                        'season_grade_ranking': rank['season_grade_ranking'],
                        'recent_win_rate': recent['recent_win_rate'],
                        'recent_kill_death_rate': recent['recent_kill_death_rate'],
                        'recent_assault_rate': recent['recent_assault_rate'],
                        'recent_sniper_rate': recent['recent_sniper_rate'],
                        'recent_special_rate': recent['recent_special_rate'],
                        'solo_rank_match_score': tier['solo_rank_match_score'],
                        'party_rank_match_score': tier['party_rank_match_score']
                    }
                    records.append(record)
            except Exception as e:
                print(f"[ERROR] 병합 에러 - {filename}: {e}")

    df_merged = pd.DataFrame(records)

    # 6. match_result 포함 병합
    match_result_only = df_match[['user_name', 'match_result', 'match_id', 'team_id']].drop_duplicates(subset=['user_name'])

    # df_final에서는 매치 승부에 직접적인 연관이 있는 컬럼 제거
    user_summary_for_merge = user_summary.drop(
        columns=['user_kda', 'user_kill', 'user_death', 'user_assist',
                 'kill_per_match', 'death_per_match', 'assist_per_match',
                 'actual_win_rate'], errors="ignore"
    )

    df_final = pd.merge(df_merged, user_summary_for_merge, on='user_name', how='inner')
    df_final = pd.merge(df_final, match_result_only, on='user_name', how='left')

    # 7. target 정의
    df_final['target'] = df_final['match_result'].map({1: 1, 2: 0, 3: 0})

    # 8. csv를 누적으로 저장할 수 있게 (컬럼 없을 때 대비)
    def save_with_append(path, new_df, subset_keys):
        for col in subset_keys:
            if col not in new_df.columns:
                new_df[col] = None
        if os.path.exists(path):
            old_df = pd.read_csv(path)
            for col in subset_keys:
                if col not in old_df.columns:
                    old_df[col] = None
            new_df = pd.concat([old_df, new_df], ignore_index=True)
            new_df.drop_duplicates(subset=subset_keys, keep="last", inplace=True)
        new_df.to_csv(path, index=False, encoding="utf-8-sig")

    save_with_append(os.path.join(analysis_dir, "df_match.csv"), df_match, ["user_name", "match_id"])
    save_with_append(os.path.join(analysis_dir, "df_merged.csv"), df_merged, ["user_name"])
    save_with_append(save_path, df_final, ["user_name", "match_id"])

    # 9. 평가용 데이터 저장
    eval_data = match_result_only.copy()
    eval_data['match_result'] = eval_data['match_result'].map({1: 1, 2: 0, 3: 0})
    save_with_append(os.path.join(analysis_dir, "match_results.csv"), eval_data, ["user_name", "match_id"])

    return df_final
