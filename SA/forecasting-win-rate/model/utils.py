# model/utils.py
import pandas as pd
import os
from model.config import importance_features  # SA/analysis/data_eda.ipynb 분석에서 나온 중요 feature 공통 사용

final_path = './analysis/df_final.csv'

def load_data(final_path=final_path, target_col='target', features=importance_features):
    # df_final.csv 파일을 찾지 못했을 경우 에러 메세지
    if not os.path.exists(final_path):
        raise FileNotFoundError(f'{final_path} 없음')

    df = pd.read_csv(final_path)

    missing_features = [f for f in features if f not in df.columns]

    # df_final에 importance feature가 없을 경우 에러 메시지
    if missing_features: 
        raise ValueError(f'해당 feature가 df_final에 없음 : {missing_features}')
    if target_col and target_col not in df.columns:
        raise ValueError(f"target col '{target_col}'이 df_final에 안보임")
    
    X = df[features]
    y = df[target_col] if target_col else None

    return (X, y) if target_col else df
