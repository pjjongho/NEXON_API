import os
import pandas as pd
import joblib
from datetime import datetime
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix
from model.config import importance_features

def run_inference(model_path, result_path, eval_path=None):
    print(f"[INFO] 모델 로드 중: {model_path}")
    model = joblib.load(model_path)

    # 데이터 로드
    df_live = pd.read_csv("./analysis/df_final.csv")
    df_results = pd.read_csv("./analysis/match_results.csv")

    # 예측용 feature 선택
    X_live = df_live[importance_features]
    predictions = model.predict(X_live)
    probabilities = model.predict_proba(X_live)[:, 1]

    # 예측 결과 추가
    df_live['predicted_target'] = predictions
    df_live['win_probability'] = probabilities

    # 문자열 타입 정제
    df_live['user_name'] = df_live['user_name'].astype(str).str.strip()
    df_live['match_id'] = df_live['match_id'].astype(str)
    df_results['user_name'] = df_results['user_name'].astype(str).str.strip()
    df_results['match_id'] = df_results['match_id'].astype(str)

    # 결과와 예측 merge
    df_results_with_preds = pd.merge(
        df_results,
        df_live[['user_name', 'match_id', 'win_probability']],
        on=["user_name", "match_id"],
        how="left"
    )

    # 팀 평균 예측
    df_team_valid = df_results_with_preds.dropna(subset=['win_probability'])
    team_avg = df_team_valid.groupby(['match_id', 'team_id'])['win_probability'].mean().reset_index()

    team_avg['predict'] = 0
    idx_max = team_avg.groupby('match_id')['win_probability'].idxmax()
    team_avg.loc[idx_max, 'predict'] = 1

    # 최종 결과 merge
    df_results_final = pd.merge(
        df_results_with_preds,
        team_avg[['match_id', 'team_id', 'predict']],
        on=['match_id', 'team_id'],
        how='left'
    )

    # timestamp 추가
    df_results_final['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    output_df = df_results_final[['timestamp', 'user_name', 'match_id', 'predict', 'win_probability']]

    # 기존 결과와 병합 후 중복 제거
    if os.path.exists(result_path):
        old_df = pd.read_csv(result_path)
        old_df['user_name'] = old_df['user_name'].astype(str).str.strip()
        old_df['match_id'] = old_df['match_id'].astype(str)
        output_df = pd.concat([old_df, output_df], ignore_index=True)
        output_df.drop_duplicates(subset=['user_name', 'match_id'], keep='last', inplace=True)

    # 저장
    output_df.to_csv(result_path, index=False, encoding="utf-8-sig")
    print(f"[INFO] 예측 결과 저장 완료: {result_path}")

    # 평가 지표 저장
    if eval_path:
        y_true = df_results_final['match_result']
        y_pred = df_results_final['predict']

        # NaN 제거
        valid_idx = y_true.notna() & y_pred.notna()
        y_true = y_true[valid_idx]
        y_pred = y_pred[valid_idx]

        if len(y_true) == 0:
            print("[WARNING] 평가 가능한 샘플이 없습니다. 평가 스킵")
            return

        acc = accuracy_score(y_true, y_pred)
        f1 = f1_score(y_true, y_pred)
        cm = confusion_matrix(y_true, y_pred)
        report = classification_report(y_true, y_pred)

        with open(eval_path, 'w') as f:
            f.write(f"Accuracy: {acc:.4f}\n")
            f.write(f"F1 Score: {f1:.4f}\n\n")
            f.write("Confusion Matrix:\n")
            f.write(str(cm) + "\n\n")
            f.write("Classification Report:\n")
            f.write(report)

        print(f"[INFO] 평가 결과 저장 완료: {eval_path}")

# 모델 개별 추론 func
def run_inference_rf():
    run_inference(
        model_path="./model/saved_models/random_forest.pkl",
        result_path="./analysis/match_results_rf.csv",
        eval_path="./analysis/eval_rf.txt"
    )

def run_inference_xgb():
    run_inference(
        model_path="./model/saved_models/xgboost.pkl",
        result_path="./analysis/match_results_xgb.csv",
        eval_path="./analysis/eval_xgb.txt"
    )

# def run_inference_lgbm():
#     run_inference(
#         model_path="./model/saved_models/lightgbm.pkl",
#         result_path="./analysis/match_results_lgbm.csv",
#         eval_path="./analysis/eval_lgbm.txt"
#     )
