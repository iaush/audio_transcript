from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from src.config import settings


SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
    
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
    with engine.connect() as conn:
        # Create the full-text search virtual table
        conn.execute(text("""
        CREATE VIRTUAL TABLE IF NOT EXISTS transcriptions_fts USING fts5(
            file_name,
            content='transcriptions',
            content_rowid='id'
        );
        """))
        #create insert, update and delete triggers
        conn.execute(text("""
        CREATE TRIGGER IF NOT EXISTS transcriptions_ai AFTER INSERT ON transcriptions
        BEGIN
            INSERT INTO transcriptions_fts(rowid, file_name)
            VALUES (new.id, new.file_name);
        END;
        """))

        conn.execute(text("""
        CREATE TRIGGER IF NOT EXISTS transcriptions_au AFTER UPDATE ON transcriptions
        BEGIN
            UPDATE transcriptions_fts
            SET file_name = new.file_name
            WHERE rowid = new.id;
        END;
        """))

        conn.execute(text("""
        CREATE TRIGGER IF NOT EXISTS transcriptions_ad AFTER DELETE ON transcriptions
        BEGIN
            DELETE FROM transcriptions_fts WHERE rowid = old.id;
        END;
        """))
