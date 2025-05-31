import pytest
from app import create_app
from app.database import Base, engine, SessionLocal
from app.models import Movie

@pytest.fixture(scope="module")
def test_client():
    # 테스트용 Flask 앱 생성
    app = create_app()
    app.config['TESTING'] = True

    # 테스트용 DB 초기화
    Base.metadata.create_all(bind=engine)

    testing_client = app.test_client()

    ctx = app.app_context()
    ctx.push()

    yield testing_client  # 테스트 함수에 전달

    # 테스트 종료 후 DB 초기화 삭제
    Base.metadata.drop_all(bind=engine)
    ctx.pop()

@pytest.fixture(scope="function")
def db_session():
    session = SessionLocal()
    yield session
    session.rollback()
    session.close()
