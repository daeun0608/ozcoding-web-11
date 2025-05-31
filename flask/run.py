from app import create_app
from app.database import Base, engine
from app import models  # models 안의 Movie 클래스를 인식시켜야 테이블 생성됨

app = create_app()

if __name__ == "__main__":
    # Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)  # 테이블 생성
    app.run(debug=True)
