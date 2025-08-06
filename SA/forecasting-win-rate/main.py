# forecasting-win-rate/main.py

from collected_data.collected_json import collected_api_save_json
from model.train_models import train_and_save
from model.inference import run_inference_rf, run_inference_xgb, run_inference_lgbm
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from model.config import rf_params, xgb_params, lgbm_params

if __name__ == "__main__":
    # 1. 데이터 수집 & 전처리
    collected_api_save_json()

    # 2. 모델 학습 & 저장
    train_and_save("random_forest", RandomForestClassifier, rf_params)
    train_and_save("xgboost", XGBClassifier, xgb_params)
    train_and_save("lightgbm", LGBMClassifier, lgbm_params)

    # 3. 모델별 추론
    run_inference_rf()
    run_inference_xgb()
    run_inference_lgbm()
