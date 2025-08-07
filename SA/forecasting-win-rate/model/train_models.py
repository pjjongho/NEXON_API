import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score, f1_score
from model.utils import load_data

def train_and_save(model_name, model_class, param_grid):
    print(f"[INFO] 모델 학습 : {model_name}")

    X, y = load_data()

    grid_search = GridSearchCV(
        estimator=model_class(),
        param_grid=param_grid,
        cv=5,
        scoring='f1',
        n_jobs=-1,
        verbose=1,
        return_train_score=True
    )
    grid_search.fit(X, y)

    best_model = grid_search.best_estimator_
    best_params = grid_search.best_params_

    y_pred = best_model.predict(X)
    acc = accuracy_score(y, y_pred)
    f1 = f1_score(y, y_pred)

    print(f"[RESULT] {model_name} Best Params: {best_params}")
    print(f"[RESULT] Train Accuracy: {acc:.4f}")
    print(f"[RESULT] Train F1 Score: {f1:.4f}")

    # 모델 저장
    joblib.dump(best_model, f'./model/{model_name}_model.pkl')

    # CV 결과 저장
    results_df = pd.DataFrame(grid_search.cv_results_)
    results_df.to_csv(f'./analysis/{model_name}_cv_results.csv', index=False)

    # 성능 상위 N개 시각화
    top_n = 5
    top_df = results_df.sort_values(by='mean_test_score', ascending=False).head(top_n)

    plt.figure(figsize=(12, 6))
    sns.barplot(x=top_df['mean_test_score'], y=top_df.index, palette='Blues_r')
    plt.xlabel('Mean F1 Score (CV)')
    plt.ylabel('Top Parameter Sets')
    plt.title(f'{model_name} - Top {top_n} CV Results')
    plt.tight_layout()
    plt.savefig(f'./analysis/{model_name}_cv_top{top_n}.png')
    plt.close()

    print(f"[INFO] 성능 시각화 저장 : ./analysis/{model_name}_cv_top{top_n}.png")
