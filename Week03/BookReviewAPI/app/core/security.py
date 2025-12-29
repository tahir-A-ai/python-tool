from passlib.context import CryptContext
from jose import jwt
from app.core.config import settings
from datetime import datetime, timedelta
from typing import Optional

# setup password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash a password
def get_password_hash(password):
    return pwd_context.hash(password)

# verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# create Access Token (JWT)
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
     # Set expiration time
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    # Add expiration claim to payload
    to_encode.update({"exp": expire})
    # encode the token
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt