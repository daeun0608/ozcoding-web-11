from app import create_app
from app.database import Base, engine

app = create_app()

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)  # 테이블 생성
    app.run(debug=True)
