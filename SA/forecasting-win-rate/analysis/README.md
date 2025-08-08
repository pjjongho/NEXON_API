## 📂 analysis/

**데이터 전처리 결과**, **모델 학습·평가 결과**, **시각화 이미지** 등을 저장하는 곳 
`utils/feature_engineering.py` 실행 이후 생성된 파일과, 모델 학습·평가 스크립트에서 출력된 결과물이 포함

---

### 📄 주요 파일 설명

| 파일명 | 설명 |
| --- | --- |
| `df_match.csv` | 매치별 참가자 단위 원본+파생 메타데이터 |
| `df_merged.csv` | API 기반 요약 지표 데이터 (basic/rank/recent/tier 병합 결과) |
| `user_summary.csv` | 유저별 누적 통계 요약 (승/무/패, KDA, 경기당 지표) |
| `df_final.csv` | **학습용 최종 데이터셋** (정보 누설 방지 피처 제외, target 포함) |
| `match_results.csv` | 매치별 승패 레이블(이진)만 저장한 데이터 |
| `match_results_rf.csv` | RandomForest 모델 추론 결과 (유저 단위) |
| `match_results_xgb.csv` | XGBoost 모델 추론 결과 (유저 단위) |
| `random_forest_cv_results.csv` | RandomForest 교차검증 성능 기록 |
| `xgboost_cv_results.csv` | XGBoost 교차검증 성능 기록 |
| `eval_rf.txt` | RandomForest 최종 학습·평가 지표 텍스트 로그 |
| `eval_xgb.txt` | XGBoost 최종 학습·평가 지표 텍스트 로그 |
| `random_forest_cv_top5.png` | RandomForest 상위 5개 피처 중요도 시각화 |
| `xgboost_cv_top5.png` | XGBoost 상위 5개 피처 중요도 시각화 |

---

### 📂 evaluation/
- 추가적인 모델 평가, 실험 결과, 보조 시각화 자료를 저장하는 서브 폴더

---

#### 💡 특징
- **데이터 전처리 → 학습 → 평가**의 전 과정 결과물이 이 폴더에 누적 저장됨
- 전처리 산출물(`df_*`)과 모델링 산출물(`match_results_*`, `eval_*.txt`, 시각화 이미지)을 한 곳에서 관리
- 이 폴더만으로도 모델 재현 및 성능 비교가 가능
