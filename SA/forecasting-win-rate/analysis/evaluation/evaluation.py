# analysis/evaluation/evaluate_models.py
def evaluate_all_models():
    import os
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    from sklearn.metrics import accuracy_score, f1_score, confusion_matrix

    models = {
        "rf": "match_results_rf.csv",
        "xgb": "match_results_xgb.csv",
    }

    eval_dir = "./analysis/evaluation"
    plot_dir = os.path.join(eval_dir, "plots")
    os.makedirs(plot_dir, exist_ok=True)

    # 정답 데이터 불러오기
    df_truth = pd.read_csv("./analysis/match_results.csv")[['user_name', 'match_id', 'match_result']]

    # 이전 summary 불러오기 (없으면 새로 생성)
    summary_path = os.path.join(eval_dir, "eval_summary.csv")
    if os.path.exists(summary_path):
        summary_df = pd.read_csv(summary_path)
        last_eval_id = summary_df["eval_id"].max()
    else:
        summary_df = pd.DataFrame(columns=["eval_id", "model", "accuracy", "f1_score", "total_length", "eval_length"])
        last_eval_id = 0

    new_rows = []

    for model_name, filename in models.items():
        df_pred = pd.read_csv(f"./analysis/{filename}")
        df = pd.merge(df_pred, df_truth, on=['user_name', 'match_id'], how='left')

        total_length = len(df)
        df = df[df['predict'].notna() & df['match_result'].notna()]
        eval_length = len(df)

        if eval_length == 0:
            print(f"[WARNING] {model_name} 모델의 유효한 평가 데이터가 없없.")
            continue

        y_true = df['match_result']
        y_pred = df['predict']
        y_prob = df['win_probability']

        acc = accuracy_score(y_true, y_pred)
        f1 = f1_score(y_true, y_pred)
        new_rows.append({
            "eval_id": last_eval_id + 1,
            "model": model_name,
            "accuracy": acc,
            "f1_score": f1,
            "total_length": total_length,
            "eval_length": eval_length
        })

        # confusion matrix 시각화
        cm = confusion_matrix(y_true, y_pred)
        plt.figure(figsize=(4, 4))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False)
        plt.title(f"{model_name.upper()} Confusion Matrix")
        plt.xlabel("Predicted")
        plt.ylabel("Actual")
        plt.tight_layout()
        plt.savefig(f"{plot_dir}/confusion_{model_name}_eval{last_eval_id + 1}.png")
        plt.close()
        print(f"[INFO] Confusion Matrix 저장 : confusion_{model_name}_eval{last_eval_id + 1}.png")

        # win_probability 분포 시각화
        plt.figure(figsize=(6, 3))
        sns.histplot(y_prob, bins=20, kde=True)
        plt.title(f"{model_name.upper()} win_probability Distribution")
        plt.xlabel("win_probability")
        plt.tight_layout()
        plt.savefig(f"{plot_dir}/win_prob_dist_{model_name}_eval{last_eval_id + 1}.png")
        plt.close()
        print(f"[INFO] Prob Distribution 저장 : win_prob_dist_{model_name}_eval{last_eval_id + 1}.png")

    # 평가 결과 누적 저장
    if new_rows:
        updated_summary = pd.concat([summary_df, pd.DataFrame(new_rows)], ignore_index=True)
        updated_summary.to_csv(summary_path, index=False)
        print(f"[INFO] Evaluation Summary 저장: {summary_path}")