# 🗂️ NEXON API 활용 프로젝트

그냥 한번 시작하고 보는 것 ㅎ.ㅎ

---

## ✅ 2025.07.16 00:42

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

---
### ✅ 2025.07.16 22:18

#### 🕸️ 닉네임 크롤링 기능 구현
- `maple.gg` 전투력 랭킹 페이지에서 상위 1000명 닉네임 수집 <span style:color="blue" (아마 상관분석을 통해 추천시스템 정도 만들어보려나 싶은 느낌적인 느낌) </span>
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

## 🧱 디렉토리 구조
```
NEXON_API/
│
├── api_request/
│ └── char_info.py # 캐릭터 API 요청 모듈
├── crawler/
│ └── nickname_crawler.py # maple.gg 크롤러
├── main.py # 전체 실행 흐름
├── .gitignore
└── api_keys.txt # API 키 저장 **(절대절대 비밀!)**
```
---

## 💡 향후 계획 체크리스트

- [ ] OCID 조회 및 캐릭터 기본 정보 수집 기능 연결
- [ ] 여러 캐릭터 정보를 `.csv`로 저장
- [ ] 도장/유니온/랭킹 API 연동 확장
- [ ] 수집 데이터 분석 및 시각화

---

## 📌 주의사항

- [x] `api_keys.txt`는 `.gitignore`에 포함되어야 함
- [x] `__pycache__/`, `.pyc` 캐시 파일도 제외
- [ ] Git 커밋 메시지는 일관성 있게 작성

---

## 📎 참고 링크

- [넥슨 Open API 공식 문서](https://open.api.nexon.com/)
