# 🎬 Flask 기반 영화 추천 웹 애플리케이션

사용자 입력을 기반으로 장르별 영화를 추천하고, 관리자 페이지에서 영화 데이터를 직접 관리할 수 있는 Flask 기반 영화 추천 웹 애플리케이션입니다.

---

## 📁 프로젝트 구조

```
project-root/
├── app/
│   ├── __init__.py         # Flask 앱 생성
│   ├── routes.py           # 라우팅 및 API
│   ├── database.py         # DB 연결 설정
│   ├── models.py           # SQLAlchemy 모델 정의
│   └── templates/          # HTML 템플릿
│       ├── index.html
│       ├── admin.html
│       └── results.html
├── run.py                  # 애플리케이션 실행 엔트리포인트
├── .env                    # 환경 변수 설정 파일
├── requirements.txt        # 의존성 패키지 목록
└── README.md
```

---

## ⚙️ 설치 및 실행

### 1. 프로젝트 클론

```bash
git clone https://github.com/yourusername/flask-movie-recommend.git
cd flask-movie-recommend
```

### 2. 가상환경 설정 및 패키지 설치

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. `.env` 파일 생성

루트 디렉토리에 `.env` 파일을 생성하고 다음 내용을 입력:

```env
DB_USER=root
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=3306
DB_NAME=moviedb
```

### 4. MySQL Docker 컨테이너 실행 (선택)

```bash
docker run --name flask-mysql -e MYSQL_ROOT_PASSWORD=yourpassword \
  -e MYSQL_DATABASE=moviedb -p 3306:3306 -d mysql:8.0
```

### 5. 서버 실행

```bash
python run.py
```

첫 실행 시 DB 테이블이 자동으로 생성됩니다.

---

## 🌐 주요 페이지 안내

| 경로            | 설명                                  |
|-----------------|---------------------------------------|
| `/`             | 사용자 추천 키워드 입력 페이지         |
| `/recommend`    | 키워드 기반 추천 API (POST 요청)       |
| `/admin`        | 영화 목록 확인 및 등록하는 관리자 페이지 |
| `/admin/add`    | 영화 추가 API (POST 요청)              |

---

## 🧪 테스트

```bash
pytest tests/
```

테스트는 API 응답 및 추천 기능의 정상 동작 여부를 검증합니다.

---

## 💡 기획 목적

- Python(Flask)을 활용한 실전 프로젝트 구조 경험
- 추천 알고리즘 및 CRUD 기능 구현 연습
- GitHub 협업 및 코드 분리/모듈화 학습
- 프론트엔드 연동을 통한 전체 웹 개발 흐름 이해

---

## 🖥️ 접속 요약

1. 서버 실행 후 웹 브라우저에서 접속:
   - 사용자 페이지: [http://localhost:5000/](http://localhost:5000/)
   - 관리자 페이지: [http://localhost:5000/admin](http://localhost:5000/admin)

2. 추천 기능은 장르 키워드로 동작 (`Comedy`, `Action` 등 입력)

---

## 📌 기타

- 이 프로젝트는 교육 목적의 샘플입니다.
- 팀 프로젝트 또는 포트폴리오 제출용으로 확장 가능합니다.