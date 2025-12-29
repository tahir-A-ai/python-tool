from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# connetion URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# 2. The Engine (The actual worker that talks to the DB)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False} #> need only in sqlite
)

# 3. The SessionLocal (The factory that creates temporary database sessions)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. The Base (The parent class for all your models)
Base = declarative_base()
""" 
    The Problem: Python classes are just code. 
    How does the database engine know that class Task should be a SQL table but class Helper should not?
    Solution: (declarative_base())
    Every model class we create will inherit this parent class (Base),
    This function returns a class (usually named Base) that maintains a Metadata Registry.
    The class inherits from Base, is automatically added to the 'Base.metadata' registry.
    Later, 'Base.metadata.create_all(bind=engine)' looks at this registry and creates only the relevant tables.
 """
