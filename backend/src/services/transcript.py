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
from sqlalchemy import text

transcriber = pipeline("automatic-speech-recognition", model="openai/whisper-tiny")

UPLOAD_DIR = Path(os.path.join("src", "uploads"))
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Transcribe the audio file based on documentaion
def file_to_text(file_content):
    transcription = transcriber(file_content)
    return transcription['text']

# Save the uploaded file and transcribe it
async def transcribe_and_save(file_name: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    unique_id = str(uuid.uuid4())
    file_extension = Path(file.filename).suffix
    file_path = Path(os.path.join(UPLOAD_DIR, f"{unique_id}{file_extension}")) #os.join to ensure compatibility with different OS

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
    
# get all transcriptions from db
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
    
# search based on search term in transcription, NOT IN USE. using FTS below  
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
    
# search based on search term using native FTS by sqlite, had to use raw query as sqlalchemy does not support FTS in sqlite 
async def search_transcriptions_fts(search_term: str, db: Session):
    search_term = ''.join(e for e in search_term if e.isalnum() or e.isspace())
    try:
        query = """
        SELECT transcriptions.id, transcriptions.file_name, transcriptions.transcription, transcriptions.upload_path, transcriptions.created
        FROM transcriptions
        JOIN transcriptions_fts ON transcriptions.id = transcriptions_fts.rowid
        WHERE transcriptions_fts MATCH :search_term;
        """
        results = db.execute(text(query), {"search_term": search_term}).all()
        print(f"Results: {results}")
        transcription_instances = []
        for row in results:
            transcription = Transcription(
                id=row[0],
                file_name=row[1],
                transcription=row[2],
                upload_path=row[3],
                created=row[4]
            )
            transcription_instances.append(transcription)

        return [{
                "file_name": transcription.file_name,
                "transcription": transcription.transcription,
                "upload_path": transcription.upload_path,
                "created": transcription.created}
                for transcription in transcription_instances]
    except Exception as e:
        print(f"Error: {e}")
        raise e
                
# delete transcription based on upload path, upload path is unique uuid
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

