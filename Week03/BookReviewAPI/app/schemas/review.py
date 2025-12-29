from pydantic import BaseModel, Field
from typing import Optional
from app.schemas.book import BookResponse
from app.schemas.user import UserResponse

class ReviewBase(BaseModel):
    book_id: int
    content: str
    rating: int = Field(..., ge=1, le=5)    

class ReviewCreate(ReviewBase):
    pass  # Inherits title, content, rating

class ReviewUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    rating: Optional[int] = None

class ReviewResponse(ReviewBase):
    id: int
    owner_id: int
    book_id: int
    is_approved: bool
    owner: UserResponse
    book: BookResponse

class Config:
    from_attributes = True