# 🎬 나만의 콘텐츠 추천기

> 사용자의 취향에 따라 콘텐츠(영화, 책 등)를 추천하는 웹 애플리케이션  
> Python(FastAPI) + JavaScript + SQLite 기반의 실전형 교육 프로젝트

---

## 🚀 주요 기능

- 🔍 키워드 기반 콘텐츠 추천 (태그 기반)
- 📋 콘텐츠 목록 (제목, 장르, 태그, 이미지 포함)
- 🧠 간단한 추천 알고리즘 탑재
- 🌐 웹 UI 연동 (설문 입력 / 추천 결과)
- ⚙️ SQLite 연동 및 FastAPI REST API 제공
- 🛠️ GitHub 기반 협업 + 코드 리팩토링 + 문서화 실습

---

## 🗂️ 프로젝트 구조
```
project-root/
├── backend/
│ ├── main.py # FastAPI 엔트리포인트
│ ├── models.py # Pydantic 모델
│ ├── recommend.py # 추천 알고리즘
│ ├── database.py # SQLite DB 설정 + ORM
│ └── data/ # 초기 콘텐츠 JSON
├── frontend/
│ ├── index.html # 설문 입력 페이지
│ ├── results.html # 추천 결과 페이지
│ └── admin.html # (확장 예정) 콘텐츠 CRUD
└── README.md
```


---

## ⚙️ 설치 및 실행

### 1. 백엔드 실행

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
