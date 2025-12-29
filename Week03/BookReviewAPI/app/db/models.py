from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_admin = Column(Boolean, default=False)

    # relationship - user can have multiple reviews
    reviews = relationship("Review", back_populates="owner")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author = Column(String)
    description = Column(String)
    book_reveiws = relationship("Review", back_populates="book")
    

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    content = Column(String)
    rating = Column(Integer)
    is_approved = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))  # a review belongs to single user
    owner = relationship("User", back_populates="reviews")
    books = relationship("books", back_populates="book_reveiws")

