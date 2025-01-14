
from src.database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi import APIRouter, UploadFile, File
from src.services.transcript import transcribe_and_save, transcription_info, search_transcription
from fastapi import HTTPException
router = APIRouter()

@router.post("/transcribe", description="Upload a audio file")
async def upload_audio(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if file.content_type not in ["audio/wav", "audio/mp3", "audio/mpeg"]:
        raise HTTPException(status_code=400, detail="Unsupported file type.")
    
    try:
        res = await transcribe_and_save(file, db)
        return res
    except Exception as e:
        return {"error": str(e)}

@router.get("/transcriptions", description="Get all transcriptions")
async def get_transcriptions(db: Session = Depends(get_db)):
    try:
        res = await transcription_info(db)
        return res
    except Exception as e:
        return {"error": str(e)}
    
@router.get("/search", description="Search for transcription that contains search term")
async def search_transcriptions(search_term: str, db: Session = Depends(get_db)):
    try:
        res = await search_transcription(search_term, db)
        return res
    except Exception as e:
        return {"error": str(e)}