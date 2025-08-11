### 📄 utils/feature_engineering.py

`match-detail` JSON과 `collected_data` 폴더의 유저 정보 JSON(basic, rank, recent, tier)을 병합·정리하여  
모델 학습에 바로 사용할 수 있는 `df_final.csv`를 생성하는 전처리 모듈
**(시간이 제일 많이 들었고 가장 힘들었던 작업..다른 모듈을 추가할때마다 계속 수정해줘야 하는 귀찮지만 꼭 해야하는 모듈)**

#### 🛠 주요 기능
1. **매치 메타데이터 추가**
   - `match_id`, `match_type`, `match_mode`, `match_map`, `date_match`를 모든 매치 유저 행에 추가  
   → 이후 병합 및 누적 저장 시 동일 경기 컨텍스트 유지

2. **경기 결과 파생 컬럼 생성**
   - `match_result`를 `is_win / is_draw / is_loss`로 변환
   - 향후 통계 계산 및 타겟 레이블 생성에 활용

3. **유저 요약 통계(user_summary) 산출**
   - 유저별 승/무/패, 킬·데스·어시스트 수 및 경기당 평균, KDA 등 계산
   - `user_summary.csv`에 누적 저장 (기존 데이터와 중복 제거)

4. **API 데이터 병합(df_merged)**
   - basic, rank, recent, tier JSON 파일을 매칭 병합
   - 주요 지표:
     - 랭킹: `grade_ranking`, `season_grade_ranking`
     - 최근 전적: `recent_win_rate`, `recent_kill_death_rate`, 포지션 비율
     - 티어 점수: `solo_rank_match_score`, `party_rank_match_score`

5. **추가 Feature 제거**
   - 경기 결과에 직접적으로 의존하는 지표(`user_kda`, `*_per_match`, `actual_win_rate`)는 학습셋에서 제외
     ```
     제외에 대한 근거는 SA/analysis/data_eda.ipynb 를 통해 매치에 직접적인 영향을 주는 컬럼과 importance feature를 통해 중요도가 높은 feature를 select
     ```

6. **최종 데이터셋(df_final) 생성**
   - `user_name`을 기준으로 user_summary와 df_merged를 병합
   - `target` 컬럼 생성 (승=1, 무/패=0) **무승부 같은 경우 기존 raw data 에서는 3으로 기록됨, 그렇다고 NaN 으로 처리하기엔 데이터가 워낙 소수라 0으로 즉, 패배로 인지하게 만듬**
   - `df_final.csv`로 저장 (기존 데이터와 중복 제거)

7. **안전한 누적 저장**
   - `df_match.csv`, `df_merged.csv`, `df_final.csv`, `match_results.csv` 모두 `['user_name', 'match_id']` 기준으로 최신 데이터만 유지

---

#### 📂 출력 파일 구조
| 파일명 | 설명 | 키 컬럼 |
| --- | --- | --- |
| `df_match.csv` | 매치 참가자 단위 원본+파생 메타 | `user_name`, `match_id` |
| `user_summary.csv` | 유저별 누적 요약 통계 | `user_name`, `match_id` |
| `df_merged.csv` | API 기반 요약 지표 | `user_name` |
| `df_final.csv` | 학습 입력 데이터셋 (누설 피처 제외, target 포함) | `user_name`, `match_id` |
| `match_results.csv` | 매치별 승패 레이블만 저장 | `user_name`, `match_id` |

---

#### 💡 특징
- **Idempotent 설계**: 여러 번 실행해도 중복 없이 최신 데이터만 유지
- **Leakage 방지**: 동일 경기에서 파생된 과도한 성능지표는 학습셋에서 제외
- **유니크 키 유지**: `['user_name','match_id']`를 전 과정에서 고유 식별자로 사용
- **원본·요약·최종셋 분리 저장**: 디버깅, 분석, 재현성 확보에 유리

---

#### 📌 사용 예시
```python
from utils.feature_engineering import feature_engineering

df = feature_engineering(
    match_path="collected_data/match-detail_json/20250808_md.json",
    save_path="analysis/df_final.csv"
)
