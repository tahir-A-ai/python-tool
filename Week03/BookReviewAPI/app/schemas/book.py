from pydantic import BaseModel
from typing import Optional

class BookBase(BaseModel):
    title: str
    author: str
    description: Optional[str]

# create schema (input)
class BookCreate(BookBase):
    pass   # Inherits everything from Base (Admins just send title/author/desc)

# Reponse schema (output)
class BookResponse(BookBase):
    id: int

class Config:
    from_attributes = True