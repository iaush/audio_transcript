from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.dialects.sqlite import INTEGER
from pydantic import BaseModel
from datetime import datetime

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db" 


engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, echo=True)

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



# class Transcription(Base):
#     __tablename__ = "transcriptions"

#     id = Column(INTEGER, primary_key=True, index=True)
#     file_name = Column(String(255), nullable=False)
#     transcription = Column(Text, nullable=True)
#     upload_path = Column(String(255), nullable=True)
#     created = Column(DateTime, default=datetime.utcnow, nullable=False)

#     def to_dict(self):
#         return{
#             "id": self.id, 
#             "file_name": self.file_name,
#             "upload_path": self.upload_path,
#             "transcription": self.transcription,
#             "created": self.created
#         }


# class TranscriptionBase(BaseModel):
#     file_name: str
#     transcription: str

# class TranscriptionCreate(TranscriptionBase):
#     pass

# class TranscriptionRead(TranscriptionBase):
#     id: int  
#     upload_path: str
#     created: datetime

#     class Config:
#         orm_mode = True
