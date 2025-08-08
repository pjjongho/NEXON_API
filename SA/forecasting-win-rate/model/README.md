## 📂 model/ 디렉토리 설명

이 디렉토리는 **승률 예측 모델의 학습·추론·설정**에 필요한 핵심 모듈

### 📄 `config.py`
- 프로젝트 전역에서 사용하는 **설정값**과 **하이퍼파라미터**를 관리.
  - 모델 저장 경로
  - 학습/평가 데이터 경로
  - K-Fold 파라미터
  - 하이퍼파라미터 그리드

### 📄 `train_models.py`
- **모델 학습 및 저장** 
  - 데이터 로드 (`.forecasting-win-rate/utils/feature_engineering` 결과 활용)
  - Stratified K-Fold 교차검증
  - GridSearchCV 기반 하이퍼파라미터 튜닝
  - 학습 완료 모델 `.pkl` 파일로 저장
- 사용 모델:
  - RandomForestClassifier
  - XGBoostClassifier

### 📄 `inference.py`
- **저장된 모델 불러와서 추론**
  - 해당 부분이 조금 특이함
    ```bash
    SA/{analysis, api_request, collected_data, crwaler}를 통해 작업한 데이터를
    **.SA/analysis/data_eda.ipynb** 를 통해 학습한 pkl 파일을 추론에 사용함 **<span style="color:orange">(사전에 학습된 파라미터가 필요했기 때문)</span>**
    
    ```
- 신규 매치 데이터에 대해 각 유저의 승리 확률 계산.
- **팀별 평균 승률(team_predict)** 산출.
- 예측 결과를 CSV로 저장.
- 저장 시 `['user_name', 'match_id']` 기준으로 중복 제거(`keep='last'`).

### 📄 `utils.py`
- 모델 학습/추론 과정에서 반복적으로 사용하는 **유틸리티 함수** 모음.
- 예:
  - 데이터 로드 및 전처리
  - 공통 지표 계산
  - 파일 저장/불러오기 헬퍼

### 📄 `__init__.py`
- `model` 디렉토리를 Python 패키지로 인식하도록 설정.

---

📌 **작업 플로우**  
1. `config.py`에서 경로·파라미터 설정  
2. `train_models.py` 실행 → 모델 학습 및 저장  
3. `inference.py` 실행 → 새 데이터 예측 및 결과 저장  
