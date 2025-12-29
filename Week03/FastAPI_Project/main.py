from fastapi import FastAPI, HTTPException,status, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import auth
from jose import JWTError, jwt
from fastapi import Request
import time
from fastapi.middleware.cors import CORSMiddleware
import models, schemas
from database import engine, SessionLocal
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from slowapi.middleware import SlowAPIMiddleware

models.Base.metadata.create_all(bind=engine)

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter

app.add_middleware(SlowAPIMiddleware)

# list of who can talk to API
origins = [
    "http://localhost:3000",  # React / Next.js
    "http://127.0.0.1:3000",
    # "*"  used to allow every origin
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # List of allowed domains
    allow_credentials=True,         # Allow cookies/auth headers
    allow_methods=["*"],            # Allow all verbs (GET, POST, etc.)
    allow_headers=["*"],            # Allow all headers (Authorization, etc.)
)


@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Too many requests"}
    )


# custom middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    # 1. BEFORE request is processed
    start_time = time.time()
    
    # 2. PASS request to the path operation (and wait for result)
    # This 'call_next' passes the ball to the next layer (or your function)
    response = await call_next(request)
    
    # 3. AFTER request is processed
    process_time = time.time() - start_time
    
    # Add a custom header to tell the client how long it took
    response.headers["X-Process-Time"] = str(process_time)
    
    return response

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Hash the password before saving!
    hashed_pwd = auth.get_password_hash(user.password)
    new_user = models.User(email=user.email, hashed_password=hashed_pwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # 1. Find user by username (we used email as username)
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    
    # 2. Check if user exists and password matches
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )     
    
    # 3. Create JWT
    access_token = auth.create_access_token(data={"sub": user.email})  # here user's email is used as an id
    return {"access_token": access_token, "token_type": "bearer"}


# This tells FastAPI: "Look for a header named Authorization"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode JWT
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    # Check if user actually exists in DB
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

# this route is protected using auth dependency i-e it will first 
# execute 'get_current_user' before executing 'read_users_me' method
@app.get("/users/me", response_model=schemas.UserResponse)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user


@app.get("/")
def home():
    return {"message": "Welcome"}

# CRUD end points
# 1. GET- Read all tasks
@app.get("/tasks", response_model=List[schemas.TaskResponse])
@limiter.limit("5/minute")
def get_tasks(
    request: Request, 
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None, 
    db: Session = Depends(get_db)):
    # starting query
    query = db.query(models.Task)
    # apply filtering if a search term is provided
    if search:
        query = query.filter(models.Task.title.contains(search))
    # applying Pagination
    # .offset() skips the first 'skip' rows, in this case 0
    # .limit() stops fetching after 'limit' rows , in this case 10
    tasks = query.offset(skip).limit(limit).all()
    return tasks

# 2. GET- Read task by id
@app.get("/tasks/{task_id}", response_model=schemas.TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found!")
    return task
    

# 3. POST - Create task
@app.post("/tasks")
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    new_task = models.Task(**task.model_dump())
    # Add to Session (Staging Area)
    db.add(new_task)
    # Commit (Save to Disk
    db.commit()
    # Refresh (Reload from DB to get the generated ID)
    db.refresh(new_task)
    
    return new_task

# 4. PUT - Update task
@app.put("/tasks/{task_id}")
def update_task(task_id: int,  task_update: schemas.TaskCreate, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found!")
    # updating fields
    db_task.title = task_update.title
    db_task.description = task_update.description
    db_task.is_completed = task_update.is_completed

    db.commit()
    db.refresh(db_task)
    return db_task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    # get the task
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # delete the object from the session
    db.delete(db_task)
    db.commit()
    return {"message": "Task deleted successfully"}