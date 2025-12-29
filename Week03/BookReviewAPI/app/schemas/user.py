from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_admin: bool

class Config:
    # this tells pydentic to read data even if it comes from an ORM obj
    from_attributes = True

