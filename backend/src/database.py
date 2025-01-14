from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from src.config import settings


SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
    
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
