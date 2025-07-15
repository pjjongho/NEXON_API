# 🗂️ NEXON API 활용 프로젝트

본 프로젝트는 넥슨 Open API를 활용하여 캐릭터 정보를 조회하고, 다양한 데이터를 수집 및 가공하는 파이프라인을 구성하는 작업입니다.

---

## ✅ 오늘의 작업 내역 (2025.07.16)

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

## 🧱 디렉토리 구조
NEXON_API/
│
├── api_request/
│ └── char_info.py # 캐릭터 정보 API 요청 모듈
├── maple_api_prac.ipynb # 실험용 노트북 파일 (업로드 안함)
├── .gitignore
├── README.md
└── api_keys.txt # API 키 저장 (보안 주의 뿌리면 안댐 절대절대)

---

## 💡 향후 계획 체크리스트

- [ ] 여러 캐릭터 데이터 일괄 수집 기능 구현
- [ ] 랭킹/도장/유니온 등의 API 연동 확장
- [ ] 수집 데이터를 기반으로 통계 시각화 및 분석

---

## 📌 주의사항 체크리스트

- [ ] `api_keys.txt`는 `.gitignore`에 등록하여 GitHub에 업로드되지 않도록 관리
- [ ] Git 커밋 시 명확한 메시지 작성 (`Move char_info.py to api_request folder` 등)

---

## 📎 참고 링크

- [넥슨 Open API 공식 문서](https://open.api.nexon.com/)
