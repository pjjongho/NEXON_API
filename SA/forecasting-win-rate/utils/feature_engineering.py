import os
import json
import pandas as pd

def feature_engineering(match_path, merged_path, save_path):
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

    # match_result 정수 변환
    df_match['match_result'] = df_match['match_result'].astype(int)

    # 3. 승/무/패 여부 컬럼
    df_match['is_win'] = df_match['match_result'].apply(lambda x: 1 if x == 1 else 0)
    df_match['is_draw'] = df_match['match_result'].apply(lambda x: 1 if x == 3 else 0)
    df_match['is_loss'] = df_match['match_result'].apply(lambda x: 1 if x == 2 else 0)

    # 4. 유저별 경기 매치 통계
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

    # 5. collected_data의 JSON 파일 로드 및 병합
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
    df_final = pd.merge(df_merged, user_summary, on='user_name', how='inner')
    df_final = pd.merge(df_final, match_result_only, on='user_name', how='left')

    # 7. 이진 분류 target 정의
    df_final['target'] = df_final['match_result'].map({1: 1, 2: 0, 3: 0})

    # 8. 저장 (절대경로 사용)
    df_match.to_csv(os.path.join(analysis_dir, "df_match.csv"), index=False)
    df_merged.to_csv(os.path.join(analysis_dir, "df_merged.csv"), index=False)
    df_final.to_csv(save_path, index=False)

    # 9. 평가용 데이터 저장
    eval_data = match_result_only.copy()
    eval_data['match_result'] = eval_data['match_result'].map({1: 1, 2: 0, 3: 0})
    eval_data_path = os.path.join(analysis_dir, "match_results.csv")
    eval_data.to_csv(eval_data_path, index=False, encoding='utf-8-sig')

    return df_final
