# 🗂️ 바람의나라 API 활용

<p align="center">
  <img src="https://blog.kakaocdn.net/dna/bNf4cM/btsKF4DNtnq/AAAAAAAAAAAAAAAAAAAAAK6ke22ku0kH6VncFJT7fiEfxeq_skFMXY4g_Rf_gcGp/img.jpg?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1753973999&allow_ip=&allow_referer=&signature=RSGKUhcwugcO0FvEIq0yF%2BVCJkI%3D" width="350"/>
</p>

---

<details>
  <summary>✅ 2025.07.23 – 프로젝트 시작 & 디렉토리 구조 정리 ⋯ 펼치기</summary>

  ### 🔧 초기 설정
  - `Baram` 폴더 아래로 전체 구조 정리
  - `api_request/` 하위에 `basic`, `id`, `stat` 별로 API 분리
  - `crawler/` 디렉토리에 닉네임 수집용 스크립트 분리
  - `data/` 폴더에 csv 저장: `ocid.csv`, `basic.csv`, `stat.csv`

</details>

<details>
  <summary>✅ 2025.07.24 – OCID 수집 및 기본 정보 확보 ⋯ 펼치기</summary>

  ### 🔍 OCID 및 기본 정보 수집
  - `nickname_crawler.py`로 닉네임 500개 수집
  - 각 닉네임 기준 OCID 수집 → `ocid.csv` 저장
  - OCID로 기본 정보, 스탯 정보 수집 → `basic.csv`, `stat.csv`

</details>

<details>
  <summary>✅ 2025.07.25 – stat 컬럼 파싱 및 병합 완료 ⋯ 펼치기</summary>

  ### 🧩 stat 컬럼 전처리 & 병합
  - `stat` 컬럼이 리스트(dict) 형태로 되어 있어 펼침 처리
  - `stat_df.csv`로 저장 (힘, 지력, 체력 등 컬럼화)
  - `character_name + server_name`을 기준으로 ocid 병합
  - `_x`, `_y` 문제 발생 → 중복 컬럼 제거 + 교집합 병합 처리
  - 최종 병합 파일 `merged_df.csv` 저장 완료!

</details>

<details>
  <summary>✅ 2025.07.25 – 중복 병합 문제 해결 ⋯ 펼치기</summary>

  ### 🧨 중복 문제 처리
  - 병합 결과 row 수가 620개로 터지는 문제 발생
  - `drop_duplicates(subset=['character_name', 'server_name'])`로 중복 제거
  - 1:N 병합 방지 성공 → `basic`, `ocid`의 구조 문제 해결
  - 지금은 완전히 정상적인 병합만 진행되도록 안정화 완료!

</details>

---
## 🧱 디렉토리 구조
Baram/
├── api_request/ # API 호출 관련 모듈
│ ├── basic/ # 캐릭터 기본 정보 조회 API
│ ├── id/ # OCID 조회 API
│ └── stat/ # 캐릭터 스탯 조회 API
├── crawler/ # 닉네임 수집용 크롤러
├── data/ # 수집된 원본 데이터 저장 경로
│ # baram_ranker.csv, ocid.csv, basic.csv, stat.csv, stat_df.csv 등
├── main_analysis/ # 병합 및 분석용 코드
│ ├── data/ # 병합된 최종 csv 저장 위치



---

## 💡 향후 계획 체크리스트

- [x] 닉네임 크롤링 및 OCID 수집
- [x] 기본 정보 / 스탯 정보 수집
- [x] stat 컬럼 파싱 및 csv 변환
- [x] 병합 로직 안정화
- [ ] 데이터 시각화 및 분석 진행

---

## ⚠️ 주의사항

- [x] `api_keys.txt`는 반드시 `.gitignore`에 포함되어야 함
- [x] 하루 1천회 API 제한 → 크롤링 분산 처리 필요

---

