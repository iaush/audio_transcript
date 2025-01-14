from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import os

IS_TESTING = "pytest" in os.getenv("PYTEST_CURRENT_TEST", "")

if IS_TESTING:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # database for testing
else:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"  #  database for prod
    
# SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"
# Initialize the engine and session
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



def init_db():
    Base.metadata.create_all(bind=engine)
