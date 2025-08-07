# model/utils.py
import pandas as pd
import os
from model.config import importance_features  # SA/analysis/data_eda.ipynb 분석에서 나온 중요 feature 공통 사용

final_path = './analysis/df_final.csv'
match_results_path = './analysis/match_results.csv'

def load_data(final_path=final_path, target_col='target', features=importance_features):
    if not os.path.exists(final_path):
        raise FileNotFoundError(f'{final_path} 없음')

    df = pd.read_csv(final_path)

    # match_results.csv 불러와서 target 생성
    if not os.path.exists(match_results_path):
        raise FileNotFoundError(f'{match_results_path} 없음')
    
    match_df = pd.read_csv(match_results_path)[['user_name', 'match_id', 'match_result']]

    # match_result를 target으로 붙이기 (user_name + match_id 기준으로 merge)
    df = df.merge(match_df, on=['user_name', 'match_id'], how='left')
    df = df.rename(columns={'match_result': target_col})

    # target이 NaN인 경우 제거
    df = df.dropna(subset=[target_col])
    df[target_col] = df[target_col].astype(int)

    missing_features = [f for f in features if f not in df.columns]
    if missing_features: 
        raise ValueError(f'해당 feature가 df_final에 없음 : {missing_features}')
    if target_col and target_col not in df.columns:
        raise ValueError(f"target col '{target_col}'이 df_final에 안보임")
    
    X = df[features]
    y = df[target_col] if target_col else None

    return (X, y) if target_col else df

