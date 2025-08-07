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
from datetime import datetime

def feature_engineering(match_path, save_path):
    analysis_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "analysis"))
    os.makedirs(analysis_dir, exist_ok=True)

    with open(match_path, 'r', encoding='utf-8') as f:
        match_detail = json.load(f)

    root_match_id = str(match_detail.get('match_id'))
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

    df_match = pd.DataFrame(match_detail['match_detail'])
    df_match['user_name'] = df_match['user_name'].astype(str).str.strip()
    df_match['match_id'] = df_match['match_id'].astype(str)
    df_match['match_result'] = df_match['match_result'].astype(int)

    df_match['is_win'] = df_match['match_result'].apply(lambda x: 1 if x == 1 else 0)
    df_match['is_draw'] = df_match['match_result'].apply(lambda x: 1 if x == 3 else 0)
    df_match['is_loss'] = df_match['match_result'].apply(lambda x: 1 if x == 2 else 0)

    user_summary = (
        df_match.groupby('user_name')[['is_win', 'is_draw', 'is_loss', 'kill', 'death', 'assist']]
        .sum()
        .reset_index()
    )
    user_summary['user_name'] = user_summary['user_name'].astype(str).str.strip()
    user_summary['total_matches'] = user_summary[['is_win', 'is_draw', 'is_loss']].sum(axis=1)
    user_summary['actual_win_rate'] = user_summary['is_win'] / user_summary['total_matches']
    user_summary['user_kda'] = (user_summary['kill'] + user_summary['assist']) / user_summary['death'].replace(0, 1)
    user_summary['user_kill'] = user_summary['kill']
    user_summary['user_death'] = user_summary['death']
    user_summary['user_assist'] = user_summary['assist']
    user_summary['kill_per_match'] = user_summary['kill'] / user_summary['total_matches']
    user_summary['death_per_match'] = user_summary['death'] / user_summary['total_matches']
    user_summary['assist_per_match'] = user_summary['assist'] / user_summary['total_matches']
    user_summary['match_id'] = root_match_id

    summary_path = os.path.join(analysis_dir, "user_summary.csv")
    if os.path.exists(summary_path):
        old_summary = pd.read_csv(summary_path)
        old_summary['match_id'] = old_summary['match_id'].astype(str)
        old_summary['user_name'] = old_summary['user_name'].astype(str).str.strip()
        user_summary = pd.concat([old_summary, user_summary], ignore_index=True)
        user_summary.drop_duplicates(subset=["user_name", "match_id"], keep="last", inplace=True)
    user_summary.to_csv(summary_path, index=False, encoding="utf-8-sig")

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
                        'user_name': str(basic.get('user_name', None)).strip(),
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
    df_merged['user_name'] = df_merged['user_name'].astype(str).str.strip()

    # match_id 포함한 유저 정보
    match_result_only = df_match[['user_name', 'match_result', 'match_id', 'team_id']].drop_duplicates(subset=['user_name', 'match_id'])

    user_summary_for_merge = user_summary.drop(
        columns=[
            'user_kda', 'user_kill', 'user_death', 'user_assist',
            'kill_per_match', 'death_per_match', 'assist_per_match',
            'actual_win_rate'
        ],
        errors="ignore"
    )

    df_final = pd.merge(df_merged, user_summary_for_merge, on='user_name', how='inner')
    df_final = pd.merge(df_final, match_result_only, on=['user_name', 'match_id'], how='left')

    df_final['match_id'] = df_final['match_id'].astype(str)
    df_final['user_name'] = df_final['user_name'].astype(str).str.strip()
    df_final['target'] = df_final['match_result'].map({1: 1, 2: 0, 3: 0})
    df_final.dropna(subset=['target'], inplace=True)

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

    eval_data = match_result_only.copy()
    eval_data['match_result'] = eval_data['match_result'].map({1: 1, 2: 0, 3: 0})
    eval_data['user_name'] = eval_data['user_name'].astype(str).str.strip()
    eval_data['match_id'] = eval_data['match_id'].astype(str)
    save_with_append(os.path.join(analysis_dir, "match_results.csv"), eval_data, ["user_name", "match_id"])

    if os.path.exists(os.path.join(analysis_dir, "user_requests_summary.csv")):
        df_pred = pd.read_csv(os.path.join(analysis_dir, "user_requests_summary.csv"))
        df_pred['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        match_results_path = os.path.join(analysis_dir, f"match_results_{root_match_id}.csv")

        if os.path.exists(match_results_path):
            old_df = pd.read_csv(match_results_path)
            df_pred = pd.concat([old_df, df_pred], ignore_index=True)
            df_pred.drop_duplicates(subset=['user_name', 'match_id'], keep='last', inplace=True)

        df_pred.to_csv(match_results_path, index=False, encoding="utf-8-sig")

    return df_final