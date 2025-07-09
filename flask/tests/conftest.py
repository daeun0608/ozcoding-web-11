# 다른 테스들이 공유해서 사용할 fixture 코드 파일

import pytest
from app import create_app
from app.database import Base, SessionLocal
from app.models import Movie
from flask import g

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

TEST_ENGINE = create_engine("sqlite:///:memory:")
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=TEST_ENGINE)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.schema = None
    Base.metadata.create_all(bind=TEST_ENGINE)
    yield
    Base.metadata.drop_all(bind=TEST_ENGINE)


@pytest.fixture(scope="module")
def test_client():
    # 테스트용 Flask 앱 생성
    app = create_app()
    app.config["TESTING"] = True

    Base.metadata.create_all(bind=TEST_ENGINE)

    @app.before_request
    def override_db():
        # Flask g 객체에 mock session 주입
        if "db" not in g:
            g.db = TestingSessionLocal()

    @app.teardown_request
    def remove_db(exception=None):
        db = g.pop("db", None)
        if db:
            db.close()

    testing_client = app.test_client()

    ctx = app.app_context()
    ctx.push()

    yield testing_client

    Base.metadata.drop_all(bind=TEST_ENGINE)
    ctx.pop()

# 기본은 function
@pytest.fixture(scope="function")
def mock_session():
    session = TestingSessionLocal()
    yield session
    session.close()
