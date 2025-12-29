from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Book Review API"
    PROJECT_VERSION: str = "1.0.0"
    
    # Database - SQLite
    DATABASE_URL: str = "sqlite:///./book_review.db"
    
    # Security (key used is dummy , will generate real one later )
    SECRET_KEY: str = "supersecretkey12345" 
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()