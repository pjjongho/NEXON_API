## 📂 collected_data/ 디렉토리 설명

 **API를 통해 수집한 원본 데이터(JSON)** 와 **가공된 CSV 데이터**를 저장하며, 수집 자동화 스크립트를 포함

---

### 📄 collected_json.py
**데이터 수집 → 저장 → 전처리(feature_engineering)** 까지 자동으로 수행하는 스크립트

#### 🔹 동작 순서
1. **닉네임 + API Key 입력**
   - `api_key.txt`에서 API 키 로드.
   - 입력한 닉네임으로 OUID 조회.
2. **매치 ID 조회**
   - 해당 유저의 최근 매치 ID 리스트 가져오기.
3. **매치 상세 정보(match-detail) 수집**
   - 첫 번째 매치의 상세 데이터를 호출.
   - 같은 매치에 포함된 모든 참가자 닉네임 수집.
4. **참가자별 API 데이터 수집**
   - 각 참가자의 `basic`, `rank`, `recent`, `tier` 정보 호출.
   - OUID와 user_name 매핑.
5. **JSON 저장**
   - `collected_data/basic_json`, `rank_json`, `recent_json`, `tier_json` 폴더에 API 결과 저장.
   - 파일명: `{수집시각}_{ouid}_{닉네임}_{API코드}.json`
6. **호출 횟수 통계 CSV 저장**
   - `user_requests_summary.csv`에 OUID별 호출 횟수 기록.
7. **매치 상세 JSON & 매치 ID JSON 저장**
   - `match-detail_json`, `match_json` 폴더에 저장.
8. **매치 상세 CSV 저장**
   - `analysis/df_match.csv`로 변환 저장.
9. **feature_engineering 실행**
   - 병합/전처리 후 최종 `df_final.csv` 생성.

---

#### 📂 JSON 수집 파일 구조
```
collected_data/
├── basic_json/
├── rank_json/
├── recent_json/
├── tier_json/
├── match_json/
├── match-detail_json/
└── user_requests_summary.csv
```


---

- **원본 데이터와 가공 데이터 모두 저장**하여 재활용 가능.
- 실행 한 번으로 모든 API 호출 및 전처리 완료.
- 추후 재학습/추론 시 `df_final.csv` 바로 사용 가능.
