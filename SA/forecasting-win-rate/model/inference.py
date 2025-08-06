import pandas as pd
import joblib
from datetime import datetime
from model.config import importance_features

def run_inference(model_path, result_path):
    # 1. 모델 불러오기
    model = joblib.load(model_path)

    # 2. 데이터 로드
    df_live = pd.read_csv("./analysis/df_final.csv")
    X_live = df_live[importance_features]

    # 3. 예측
    probabilities = model.predict_proba(X_live)[:, 1]
    predictions = model.predict(X_live)

    df_live['predicted_target'] = predictions
    df_live['win_probability'] = probabilities

    # 4. match_results.csv 로드
    df_results = pd.read_csv("./analysis/match_results.csv")

    # --- NaN match_id 제거 (팀 단위 보정 안전하게) ---
    df_results = df_results.dropna(subset=['match_id'])
    df_live = df_live.dropna(subset=['match_id']) if 'match_id' in df_live.columns else df_live

    # 5. 병합
    df_results = pd.merge(
        df_results,
        df_live[['user_name', 'predicted_target', 'win_probability']],
        on="user_name", how="left"
    ).rename(columns={"predicted_target": "predict"})

    # 6. 팀 단위 보정
    # NaN match_id 제거
    df_results = df_results.dropna(subset=['match_id', 'team_id', 'win_probability'])

    team_avg = df_results.groupby(['match_id', 'team_id'])['win_probability'].mean().reset_index()
    team_avg['team_predict'] = 0

    # idxmax에서 NaN 제거
    idx_max = team_avg.groupby('match_id')['win_probability'].idxmax()
    idx_max = idx_max.dropna().astype(int)

    team_avg.loc[idx_max, 'team_predict'] = 1

    df_results = pd.merge(
        df_results.drop(columns=['predict'], errors='ignore'),
        team_avg[['match_id', 'team_id', 'team_predict']],
        on=['match_id', 'team_id'], how='left'
    ).rename(columns={'team_predict': 'predict'})

    # 7. 저장
    df_results['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    output_df = df_results[['timestamp', 'user_name', 'match_id', 'predict', 'win_probability']]
    output_df.to_csv(result_path, index=False, encoding="utf-8-sig")

    print(f"[INFO] Inference 완료: {result_path}")


def run_inference_rf():
    run_inference(
        model_path="./model/saved_models/random_forest.pkl",
        result_path="./analysis/match_results_rf.csv"
    )


def run_inference_xgb():
    run_inference(
        model_path="./model/saved_models/xgboost.pkl",
        result_path="./analysis/match_results_xgb.csv"
    )


def run_inference_lgbm():
    run_inference(
        model_path="./model/saved_models/lightgbm.pkl",
        result_path="./analysis/match_results_lgbm.csv"
    )
