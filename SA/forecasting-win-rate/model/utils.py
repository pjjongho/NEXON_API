# df_final.csv 파일을 활용해 모델에 들어갈 데이터 전처리

import pandas as pd
import os

# SA/analysis/data_eda.ipynb에서 작업하면서
# rf를 통해 importance feature를 확인한 결과
# 아래와 같은 feature가 주요 feature들로 확인됨

importance_features = [
    'user_kill', 'user_death', 'user_assist', 'total_matches', 'user_kda', 
    'kill_per_match', 'death_per_match', 'assist_per_match',
    'grade_ranking', 'season_grade_ranking', 'recent_win_rate',
    'recent_kill_death_rate', 'recent_assault_rate', 'recent_sniper_rate',
    'recent_special_rate', 'solo_rank_match_score', 'party_rank_match_score'
]

final_path = './analysis/df_final.csv'

def load_data(final_path=final_path, target_col='target'):
    
    # df_final.csv 파일을 찾지 못했을 경우 에러 메세지
    if not os.path.exists(final_path):
        raise FileNotFoundError(f'{final_path} 없음')
    
    df = pd.read_csv(final_path)

    missing_features = [f for f in importance_features if f not in df.columns]

    # df_final에 importance feature가 없을 경우 에러 메시지
    if missing_features: 
        raise ValueError(f'해당 feature가 df_final에 없음 : {missing_features}')
    if target_col not in df.columns:
        raise ValueError(f"target col '{target_col}'이 df_final에 안보임")
    
    X = df[importance_features]
    y = df[target_col]

    return X, y