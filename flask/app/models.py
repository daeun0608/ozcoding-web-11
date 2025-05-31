from sqlalchemy import Column, Integer, String, Text
from .database import Base

class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    genre = Column(String(100))
    thumbnail = Column(Text)
    description = Column(Text)