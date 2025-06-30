from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from models import UserInput, ContentItem
from recommend import recommend
from database import init_db, SessionLocal, Content
import json

app = FastAPI()
init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/recommend", response_model=list[ContentItem])
def get_recommendation(user_input: UserInput, db: Session = Depends(get_db)):
    db_items = db.query(Content).all()
    contents = [
        {
            "id": item.id,
            "title": item.title,
            "genre": item.genre,
            "tags": json.loads(item.tags),
            "thumbnail": item.thumbnail
        }
        for item in db_items
    ]
    return recommend(user_input.preference, contents)