import pandas as pd
import joblib

# 사용할 feature 리스트
importance_features = [
    'user_kill', 'user_death', 'user_assist', 'total_matches', 'user_kda',
    'kill_per_match', 'death_per_match', 'assist_per_match',
    'grade_ranking', 'season_grade_ranking', 'recent_win_rate',
    'recent_kill_death_rate', 'recent_assault_rate', 'recent_sniper_rate',
    'recent_special_rate', 'solo_rank_match_score', 'party_rank_match_score'
]

# 1. 저장된 모델 불러오기
model = joblib.load("./model/saved_models/random_forest.pkl")

# 2. 실시간 데이터 로드
df_live = pd.read_csv("./analysis/df_final.csv")

# 3. 예측용 데이터 준비
X_live = df_live[importance_features]

# 4. 승리 확률 계산
if hasattr(model, "predict_proba"):
    probabilities = model.predict_proba(X_live)[:, 1]  # positive(승) 클래스 확률
else:
    decision_vals = model.decision_function(X_live)
    probabilities = (decision_vals - decision_vals.min()) / (decision_vals.max() - decision_vals.min())

predictions = model.predict(X_live)

df_live['predicted_target'] = predictions
df_live['win_probability'] = probabilities

# 5. match_results.csv 로드
df_results = pd.read_csv("./analysis/match_results.csv")  # user_name, match_result, match_id, team_id

# 6. 예측 결과 병합 (확률까지 같이 붙임)
df_results = pd.merge(
    df_results,
    df_live[['user_name', 'predicted_target', 'win_probability']],
    on="user_name", how="left"
)

# 7. 컬럼명 변경
df_results.rename(columns={"predicted_target": "predict"}, inplace=True)

# ---------------- 팀 단위 승패 보정 로직 ----------------
team_avg = df_results.groupby(['match_id', 'team_id'])['win_probability'].mean().reset_index()
team_avg['team_predict'] = 0
team_avg.loc[team_avg.groupby('match_id')['win_probability'].idxmax(), 'team_predict'] = 1

df_results = pd.merge(
    df_results.drop(columns=['predict'], errors='ignore'),
    team_avg[['match_id', 'team_id', 'team_predict']],
    on=['match_id', 'team_id'],
    how='left'
)

df_results.rename(columns={'team_predict': 'predict'}, inplace=True)
# ----------------------------------------------------------

# 8. match_results.csv 저장
df_results.to_csv("./analysis/match_results.csv", index=False, encoding="utf-8-sig")
print('match_results.csv 저장')

# 9. 승리 확률 포함된 별도 파일 저장 
prob_output_path = "./analysis/pred_prob.csv"
df_live[['user_name', 'predicted_target', 'win_probability']].to_csv(prob_output_path, index=False, encoding='utf-8-sig')
print(f"[INFO] 승리 확률 포함 예측 결과 저장: {prob_output_path}")
