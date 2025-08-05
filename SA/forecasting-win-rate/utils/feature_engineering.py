import os
import json
import pandas as pd

def feature_engineering(match_path, merged_path, save_path):
    # 1. match_detail 로드
    with open(match_path, 'r', encoding='utf-8') as f:
        match_detail = json.load(f)

    # 2. match_detail → df_match 변환
    df_match = pd.DataFrame(match_detail['match_detail'])

    # 문자열로 저장된 match_result를 정수형으로 변환
    df_match['match_result'] = df_match['match_result'].astype(int)

    # 3. 승/무/패 여부 컬럼 생성
    df_match['is_win'] = df_match['match_result'].apply(lambda x: 1 if x == 1 else 0)
    df_match['is_draw'] = df_match['match_result'].apply(lambda x: 1 if x == 3 else 0)
    df_match['is_loss'] = df_match['match_result'].apply(lambda x: 1 if x == 2 else 0)

    # 4. 유저별 경기 요약 통계
    user_summary = df_match.groupby('ouid')[['is_win', 'is_draw', 'is_loss', 'kill', 'death', 'assist']].sum().reset_index()
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
    for filename in os.listdir("./collected_data"):
        if filename.endswith("basic.json"):
            ouid = filename.split("_")[0]
            try:
                with open(f"./collected_data/{ouid}_basic.json", encoding='utf-8') as f1, \
                     open(f"./collected_data/{ouid}_rank.json", encoding='utf-8') as f2, \
                     open(f"./collected_data/{ouid}_recent.json", encoding='utf-8') as f3, \
                     open(f"./collected_data/{ouid}_tier.json", encoding='utf-8') as f4:
                    basic = json.load(f1)
                    rank = json.load(f2)
                    recent = json.load(f3)
                    tier = json.load(f4)

                    record = {
                        'user_name': basic['user_name'],
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
                print(f"[SKIP] 병합 중 오류 발생 - {ouid}: {e}")

    df_merged = pd.DataFrame(records)

    # 6. match 통계와 병합
    df_final = pd.merge(df_merged, user_summary, on='ouid', how='inner')

    # 7. 이진 분류 target 정의
    mean_win_rate = df_final['actual_win_rate'].mean()
    df_final['target'] = (df_final['actual_win_rate'] >= mean_win_rate).astype(int)

    # 8. 저장
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    df_match.to_csv("./analysis/df_match.csv", index=False)
    df_merged.to_csv("./analysis/df_merged.csv", index=False)
    df_final.to_csv(save_path, index=False)

    return df_final
