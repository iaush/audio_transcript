from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.dialects.sqlite import INTEGER
from pydantic import BaseModel
from datetime import datetime
from src.database import Base, engine
from typing import List, Optional

class Transcription(Base):
    __tablename__ = "transcriptions"

    id = Column(INTEGER, primary_key=True, index=True)
    file_name = Column(String(255), nullable=False)
    transcription = Column(Text, nullable=True)
    upload_path = Column(String(255), nullable=True)
    created = Column(DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return{
            "id": self.id, 
            "file_name": self.file_name,
            "upload_path": self.upload_path,
            "transcription": self.transcription,
            "created": self.created
        }

class TranscriptionBase(BaseModel):
    file_name: Optional[str]
    transcription: str

class TranscriptionCreate(TranscriptionBase):
    pass

class TranscriptionRead(TranscriptionBase):
    upload_path: str
    created: datetime

    class Config:
        from_attributes = True

