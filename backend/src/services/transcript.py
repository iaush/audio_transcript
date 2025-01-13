import os
from src.models.transcription import Transcription
from src.database import get_db
from transformers import pipeline
from fastapi import UploadFile, File, Depends
from sqlalchemy.orm import Session
from pathlib import Path
from datetime import datetime, timedelta
import aiofiles
import uuid


transcriber = pipeline("automatic-speech-recognition", model="openai/whisper-tiny")

UPLOAD_DIR = Path("src/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)



def file_to_text(file_content):
    transcription = transcriber(file_content)
    print('Transcription', transcription)
    return transcription['text']

async def transcribe_and_save(file: UploadFile = File(...), db: Session = Depends(get_db)):
    unique_id = str(uuid.uuid4())
    file_extension = Path(file.filename).suffix
    file_path = UPLOAD_DIR / f"{unique_id}{file_extension}"

    # Save the uploaded file locally to play it back
    try:
        async with aiofiles.open(file_path, "wb") as buffer:
            data = await file.read()
            await buffer.write(data)
        print(f"File saved at: {file_path}")
    except Exception as e:
        print(f"Error saving file: {e}")
        raise

    transcription_text = file_to_text(data)
    transcript = Transcription(
        file_name=file.filename,
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