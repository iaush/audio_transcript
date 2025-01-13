
from src.database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi import APIRouter, UploadFile, File
from src.services.transcript import transcribe_and_save

router = APIRouter()

@router.post("/", description="Upload a audio file")
async def upload_audio(file: UploadFile = File(...), db: Session = Depends(get_db)):
    return await transcribe_and_save(file, db)

    