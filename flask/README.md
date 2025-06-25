# Flask 기반 콘텐츠 추천 프로젝트

사용자의 관심 키워드를 기반으로 콘텐츠 추천하는 프로젝트

---

# 주요기능

- 키워드 기발 콘텐츠 추천 시스템 (키워드를 입력 -> 추쳔 결과 제공)
- 추천 결과 페이지 기본 정보 제공

# 프로젝트 구조

```
root-dir/
├──app/ #flask 파일
├──tests/ #test 파일
├──README.md
├──.env #필요한 환경변수
├──run.py #프로젝트 실행
└──requirements.txt #의존성 패키지 파일
```

# 설치 및 실행

## 1. 프로젝트 클론

```
git clone GITHUB_REPO
cd flask
```

## 2. 가상환경 설정 및 패키지 설치

```
python -m venv .venv
source .venv/bin/activate #Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 3. .env 파일 생성

```
KEY = VALUE
```

## 4. 서버 실행

```
python3 run.py
```

# 구동을 위해서 필요한 환경설정(MySQL 실행)

```
docker run --name flask-mysql -e MYSQL_ROOT_PASSWORD=yourpassword \
  -e MYSQL_DATABASE=moviedb -p 3306:3306 -d mysql:8.0
```

# 주요 페이지 안내

| 경로       | 설명                             |
| ---------- | -------------------------------- |
| `/`        | 사용자 추천 키워드 입력 페이지   |
| `/admin`   | 관리자가 콘텐츠 등록 페이지      |
| `/results` | 사용자가 입력한 결과 추천 페이지 |

# API 안내

## 콘텐츠 추천 API
| MEHTOD | 경로            | 설명            |
| ------ | --------------- | --------------- |
|POST|/recommend|입력한 키워드 기반 콘텐츠 조회 API|

## 콘텐츠 매니징 API
| MEHTOD | 경로            | 설명            |
| ------ | --------------- | --------------- |
| POST   | /admin/content/ | 콘텐츠 등록 API |
| GET    | /admin/content/ | 콘텐츠 조회 API |
| DELETE | /admin/content/ | 콘텐츠 삭제 API |

# 테스트

```
pytest
```

## 기획 목적

- Python(Flask) 활용한 실습 프로젝트
- 사용자 키워드 기반 추천 프로젝트

## 요약(프로젝트 접속)

1. 서버 실행 후 브라우저 접속

- 사용자 페이지: [http://localhost:5000/](http://localhost:5000/)
- 관리자 페이지: [http://localhost:5000/admin](http://localhost:5000/admin)

## 기타
