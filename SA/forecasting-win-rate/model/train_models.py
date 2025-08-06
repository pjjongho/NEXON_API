import os
import joblib
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from sklearn.model_selection import StratifiedKFold, GridSearchCV
from sklearn.metrics import make_scorer, f1_score
from model.utils import load_data
from model.config import rf_params, xgb_params, lgbm_params

def train_and_save(model_name, model_cls, param_grid):
    X, y = load_data()

    # 샘플 수 확인
    if len(X) < 500:
        print(f"[SKIP] 데이터 길이 부족 최소 500개 이상 되어야 학습 가능 현재 길이 {len(X)}")
        return

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    scorer = make_scorer(f1_score)

    grid_search = GridSearchCV(
        estimator=model_cls(),
        param_grid=param_grid,
        cv=cv,
        scoring=scorer,
        n_jobs=-1,
        verbose=2
    )

    grid_search.fit(X, y)
    best_model = grid_search.best_estimator_

    save_dir = "./model/saved_models"
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, f"{model_name}.pkl")
    joblib.dump(best_model, save_path)

    print(f"[INFO] best params : {grid_search.best_params_}")
    print(f"[INFO] best f1 score : {grid_search.best_score_}")

if __name__ == "__main__":
    train_and_save("random_forest", RandomForestClassifier, rf_params)
    train_and_save("xgboost", XGBClassifier, xgb_params)
    train_and_save("lightgbm", LGBMClassifier, lgbm_params)
