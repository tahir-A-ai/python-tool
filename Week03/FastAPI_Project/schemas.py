from pydantic import BaseModel, ConfigDict
from typing import Optional

# User Registration, > user send this
class UserCreate(BaseModel):
    email: str
    password: str

# For reponse , > we return this (no password)
class UserResponse(BaseModel):
    id: int
    email: str

    model_config = ConfigDict(from_attributes=True)

# For Toekn, (JWT Response)
class Token (BaseModel):
    access_token: str
    token_type: str


# 1. Base Schema (Shared properties)
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    is_completed: bool = False

# 2. Create Schema (What user sends to us)
# Exact same as Base for now
class TaskCreate(TaskBase):
    pass

# 3. Response Schema (What we return to user)
class TaskResponse(TaskBase):
    id: int # The DB has an ID, but the user didn't send one.

    # THIS IS THE MAGIC CONFIG!
    # It tells Pydantic: "It's okay to read data from a SQLAlchemy object"
    # (In Pydantic V1 this was 'orm_mode = True')
    model_config = ConfigDict(from_attributes=True)

