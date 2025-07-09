from database import SessionLocal, Content, init_db
import json

def seed():
    init_db()
    db = SessionLocal()
    db.query(Content).delete()
    db.add_all([
        Content(
            title="Interstellar",
            genre="Sci-Fi",
            tags=json.dumps(["space", "future", "time"]),
            thumbnail="https://upload.wikimedia.org/wikipedia/ko/b/b7/%EC%9D%B8%ED%84%B0%EC%8A%A4%ED%85%94%EB%9D%BC.jpg"
        ),
        Content(
            title="Inception",
            genre="Thriller",
            tags=json.dumps(["dream", "heist", "mind"]),
            thumbnail="https://upload.wikimedia.org/wikipedia/ko/1/1d/%EC%9D%B8%EC%85%89%EC%85%98.jpg"
        )
    ])
    db.commit()
    db.close()

if __name__ == "__main__":
    seed()