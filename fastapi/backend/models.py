from pydantic import BaseModel
from typing import List

class UserInput(BaseModel):
    preference: str

class ContentItem(BaseModel):
    id: int
    title: str
    genre: str
    tags: List[str]
    thumbnail: str