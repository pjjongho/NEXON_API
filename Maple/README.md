# 🗂️ Maple API 활용

<p align="center">
  <img src="https://image.ytn.co.kr/general/jpg/2021/0311/202103110915014429_d.jpg" width="350"/>
</p>

그냥 한번 시작하고 보는 것 ㅎ.ㅎ

---
<details>
  <summary>✅ 2025.07.16 00:42 – 초기 설정 ⋯ 펼치기</summary>

  ### 🔧 초기 설정

  - `git init`으로 Git 저장소 초기화  
  - GitHub 원격 저장소 연결 (`origin/main`)  
  - 첫 커밋 완료 및 `push` 성공

  ### 📁 디렉토리 구조 정비

  - 기존 `char_info.py` 파일을 `api_request/char_info.py`로 이동  
    → **API 호출 관련 모듈을 별도 폴더로 정리**

  ### 📡 API 호출 준비

  - `api_keys.txt`를 통한 인증 키 로딩 구현  
  - 넥슨 Open API를 통해 캐릭터 OCID 검색 및 정보 조회 구조 준비

</details>

<details>
  <summary>✅ 2025.07.16 22:18 – 닉네임 크롤링 기능 구현 ⋯ 펼치기</summary>

  #### 🕸️ 닉네임 크롤링 기능 구현
  - `maple.gg` 전투력 랭킹 페이지에서 상위 1000명 닉네임 수집  
    `(아마 상관분석을 통해 추천시스템 정도 만들어보려나 싶은 느낌적인 느낌)`
  - `crawler/nickname_crawler.py` 모듈 작성
  - BeautifulSoup으로 `/u/{nickname}` 형태의 `href`를 파싱

  #### 🧪 수집 결과 검증
  - 닉네임 리스트를 `pandas.DataFrame`으로 시각적으로 확인
  - `main.py`에서 수집-확인 로직 실행

  #### 🔧 Git 설정 개선
  - `.gitignore` 파일 수정:
    - `api_keys.txt`, `__pycache__/`, `*.pyc` 등 민감/불필요 파일 제외
  - VSCode 내 커밋 메시지 작성 방식 학습
  - Git CLI에서 상태 확인, add → commit → push 실습

</details>

<details>
  <summary>✅2025.07.17 - 문제발견 ㅠ ⋯ 펼치기</summary>

  #### 호출 부하에 따른 문제 발견
  - API 호출량을 인지하지 못함 (하루 1천개 호출인데, 욕심이 너무 과했음)
  - 디렉토리 구조를 전반적으로 수정
  - API를 통해 수집하는 스크립트를 나누어서 진행
  - 수집된 csv 파일도 나누어서 진행
  
</details>

<details>
  <summary>✅2025.07.18 - API 호출량 때문에 계획 수정 ⋯ 펼치기</summary>

  #### 호출량 제한으로 인해 계획 변경
  - API 호출량이 하루 1천회 하루에 하나씩 나눠서 진행
  - 데이터를 분석하기 위해 살펴보니 테스트용으로 500명 호출한 결과 164 명에 대한 정보만 호출됨
  - 원하는 API 하나하나 천천히 수집할 것.
  - 쉽지 않ㄴ ㅔ..ㅇㅁㅇ
</details>

<details>
  <summary>✅2025.07.19 - Docker 적용 ⋯ 펼치기</summary>

  #### Docker를 활용해 외부에서 작업할 수 있도록 설정
  1. Dockerfile 작성 - `Ubuntu 환경`
  2. Docker Image Build - `docker build -t nexon-api. `
  3. Jupyter Notebook 실행
    
  ```bash
  git clone https://github.com/pjjongho/NEXON_API.git
  cd NEXON_API
  docker build -t nexon-api . && docker run -p 8888:8888 -v ${PWD}:/app nexon-api
  ```
  
</details>

<details>
  <summary>✅2025.07.20 - Symbol Info 추가 ⋯ 펼치기</summary>

  #### Add Symbol API
  - Symbol API를 새로 호출하여 데이터를 추가
  - 도커 업로드 완료
  - 총 다섯개의 API 호출
  - 더이상 API 호출하지 않고 분석 및 머신러닝, 딥러닝 진행
  
</details>

<details>
  <summary>✅2025.07.21 - Data 병합 (드디어)  ⋯ 펼치기</summary>

  ### Data 병합
  - Key값은 maple.gg에서 크롤링한 nickname으로 하고 Inner Join
  - stat 이랑 symbol 같은 경우 컬럼이 딕셔너리 형태로 구성되어 있어서 까다로웠음
  - 그래도 원하는대로 해냄 ㅎㅎ 뿌-듯
  
</details>

<details>
  <summary>✅2025.07.23 - 모든 데이터 스케일링 및 변환 ⋯ 펼치기</summary>

  ### 지금까지?
  - 수집한 데이터들을 로그 변환 및 스케일링 진행
  - RandomForest 모델에 dojang_best_floor 를 타겟으로 실행해봄
  - 처참한 결과...
  - 설레는 마음으로 돌렸으나 예측을 전혀 못함.
  - Feature Engineering을 좀 더 잘 해볼 것
</details>
---

## 🧱 디렉토리 구조
```
Maple/
├── api_request/        # 넥슨 API 요청 함수들 모음 (API별로 정리해둠)
├── crawler/            # maple.gg에서 닉네임 수집하는 크롤러
├── data/               # 수집한 csv 데이터 저장하는 곳
├── dojang_analysis/    # 무릉도장 관련 분석이나 데이터 병합용 스크립트
├── scripts/            # API별 수집 스크립트들 (01_get_*.py처럼 순서대로)
├── .gitignore          # api_key 같은 민감한 파일은 커밋 안 되게 설정함
├── Dockerfile          # 도커로 실행할 수 있도록 환경 정의한 파일
├── main.py             # 일단 진입점인데 아직 손봐야 함
└── README.md           
```
---

## 💡 향후 계획 체크리스트

- [x] OCID 조회 및 캐릭터 기본 정보 수집 기능 연결 (0716)
- [x] 여러 캐릭터 정보를 `.csv`로 저장 (0717)
- [x] 도장/유니온/랭킹 API 연동 확장 (일단 코드는 완성)
- [x] Docker 활용
- [x] Data 병합 (0721)
- [ ] 수집 데이터 분석 및 시각화

---

## 📌 주의사항

- [x] `api_keys.txt`는 `.gitignore`에 포함되어야 함
- [x] `API 호출량` 꼬옥 신경쓸것

---

