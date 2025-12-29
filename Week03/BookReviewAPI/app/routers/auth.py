from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import jwt, JWTError

# local imports
from app.db.database import get_db
from app.db.models import User
from app.schemas.user import UserCreate, UserResponse
from app.core.config import settings
from app.core.security import verify_password, create_access_token, get_password_hash

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

# Sagger UI helper - it just redirect credentials to 'tokenURL' path.
# when user hits 'Authorize' on Swagger UI, the credebtials are sent to '/auth/login' endpoint to get a token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode JWT
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    # Check if user actually exists in DB
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    # 'user' obj is returned to the endpoint where is it called!
    return user


# ENDPOINT - REGISTER
@router.post("/register", response_model= UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # checking if email exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash user plain password
    hashed_pwd = get_password_hash(user.password)
    
    # creating DB Object
    new_user = User(email=user.email, hashed_password=hashed_pwd)
    
    # saving new_user to DB
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


# ENDPOINT - LOGIN
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # finding user (here email is treated as username)
    print(form_data.username)
    user = db.query(User).filter(User.email == form_data.username).first()
    print(user)
    
    # verifying Password
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # creating JWT
    access_token = create_access_token(data={"sub": user.email})
    
    # return Token along with Admin Status (for frontend)
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "is_admin": user.is_admin
    }