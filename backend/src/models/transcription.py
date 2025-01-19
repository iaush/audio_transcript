from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.sqlite import INTEGER
from pydantic import BaseModel
from datetime import datetime
from src.database import Base, engine
from typing import List, Optional
from sqlalchemy.orm import relationship

#pydantic model for transcription
class Transcription(Base):
    __tablename__ = "transcriptions"

    id = Column(Integer, primary_key=True)
    file_name = Column(String(255), nullable=False)
    transcription = Column(Text, nullable=True)
    upload_path = Column(String(255), nullable=True)
    created = Column(DateTime, default=datetime.utcnow, nullable=False)

    # fts_entry = relationship("TranscriptionFTS", back_populates="transcriptions", primaryjoin="Transcription.id==TranscriptionFTS.rowid", cascade="all, delete-orphan")

    def to_dict(self):
        return{
            "id": self.id, 
            "file_name": self.file_name,
            "upload_path": self.upload_path,
            "transcription": self.transcription,
            "created": self.created
        }
    
# class TranscriptionFTS(Base):
#     __tablename__ = "transcriptions_fts"

#     rowid = Column(Integer, ForeignKey("transcriptions.id"), primary_key=True)
#     file_name = Column(String)
#     transcription = Column(Text)

#     transcriptions = relationship("Transcription", back_populates="fts_entry", primaryjoin="Transcription.id==TranscriptionFTS.rowid")

#models for servicees
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

