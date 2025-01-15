import os
from src.models.transcription import Transcription, TranscriptionRead
from src.database import get_db
from transformers import pipeline
from fastapi import UploadFile, File, Depends
from sqlalchemy.sql import select
from sqlalchemy.orm import Session
from pathlib import Path
from datetime import datetime, timedelta
import aiofiles
import uuid
from typing import List
from fastapi import FastAPI, UploadFile, File, Depends
from fastapi.staticfiles import StaticFiles


transcriber = pipeline("automatic-speech-recognition", model="openai/whisper-tiny")

UPLOAD_DIR = Path(os.path.join("src", "uploads"))
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def file_to_text(file_content):
    transcription = transcriber(file_content)
    return transcription['text']

async def transcribe_and_save(file_name: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    unique_id = str(uuid.uuid4())
    file_extension = Path(file.filename).suffix
    file_path = Path(os.path.join(UPLOAD_DIR, f"{unique_id}{file_extension}"))

    # Save the uploaded file locally to play it back
    try:
        async with aiofiles.open(file_path, "wb") as buffer:
            data = await file.read()
            await buffer.write(data)
        print(f"File saved at: {file_path}")
    

        transcription_text = file_to_text(data)
        transcript = Transcription(
            file_name=file_name,
            upload_path=str(file_path),
            transcription=transcription_text,
            created=datetime.utcnow()+timedelta(hours=8)  
        )

        # Add the transcription to the database
        db.add(transcript)
        db.commit()
        db.refresh(transcript)
        
        return {
        "id": transcript.id,
        "file_name": transcript.file_name,
        "upload_path": transcript.upload_path,
        "transcription": transcript.transcription,
        "created": transcript.created
        }
    except Exception as e:
        print(f"Error: {e}")
        raise e
    
async def transcription_info(db: Session = Depends(get_db)) -> List[TranscriptionRead]:
    try:
        query = select(Transcription)
        transcriptions = db.execute(query).scalars().all()
        return [{
                "file_name": transcription.file_name,
                "transcription": transcription.transcription,
                "upload_path": transcription.upload_path,
                "created": transcription.created}
                for transcription in transcriptions]
    except Exception as e:
        print(f"Error: {e}")
        raise e
    
async def search_transcription(search_term: str, db: Session = Depends(get_db)) -> List[TranscriptionRead]:
    try:
        search_term = search_term.strip()
        query = select(Transcription).where(Transcription.transcription.contains(search_term))
        transcriptions = db.execute(query).scalars().all()
        return [{
                "file_name": transcription.file_name,
                "transcription": transcription.transcription,
                "upload_path": transcription.upload_path,
                "created": transcription.created}
                for transcription in transcriptions]
    except Exception as e:
        print(f"Error: {e}")
        raise e
                
async def delete_transcription_path(upload_path: str, db: Session = Depends(get_db)):
    try:
        query = select(Transcription).where(Transcription.upload_path.contains(upload_path))
        transcription = db.execute(query).scalar_one()
        db.delete(transcription)
        db.commit()

        # Delete the file from the filesystem
        os.remove(upload_path)
        print(f"File deleted at: {upload_path}")

        return {"message": "Transcription deleted"}
    except Exception as e:
        print(f"Error: {e}")
        raise e

