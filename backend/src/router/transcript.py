
from src.database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi import APIRouter, UploadFile, File, Form
from src.services.transcript import transcribe_and_save, transcription_info, search_transcription, delete_transcription_path, search_transcriptions_fts
from fastapi import HTTPException
from typing import List

router = APIRouter()

# @router.post("/transcribe", description="Upload an audio file")
# async def upload_audio(file_name: str = Form(...), file: UploadFile = File(...), db: Session = Depends(get_db)):
#     if file.content_type not in ["audio/wav", "audio/mp3", "audio/mpeg"]:
#         raise HTTPException(status_code=400, detail="Unsupported file type.")
    
#     try:
#         res = await transcribe_and_save(file_name,file , db)
#         return res
#     except Exception as e:
#         return {"error": str(e)}

#checks file type and accepts audio file to be transcribed
@router.post("/transcribe", description="Upload an audio file")
async def upload_audio(file_names: List[str] = Form(...), files: List[UploadFile] = File(...), db: Session = Depends(get_db)):
    for file in files:
        if file.content_type not in ["audio/wav", "audio/mp3", "audio/mpeg"]: #check if file type is supported audio file
            raise HTTPException(status_code=400, detail="Unsupported file type.")
    
    try:
        # print(f"Files: {files}")
        # print(f"File names: {file_names}")
        results = []
        for file, file_name in zip(files, file_names):
            res = await transcribe_and_save(file_name, file, db) #transcribe and save audio file in local folder
            results.append(res)
        return results
    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)}

#return all transcriptions in db
@router.get("/transcriptions", description="Get all transcriptions")
async def get_transcriptions(db: Session = Depends(get_db)):
    try:
        res = await transcription_info(db)
        return res
    except Exception as e:
        return {"error": str(e)}

#search for transcription that contains search term in file name
@router.get("/search", description="Search for transcription that contains search term")
async def search_transcriptions(search_term: str, db: Session = Depends(get_db)):
    try:
        # res = await search_transcription(search_term, db)
        res = await search_transcriptions_fts(search_term, db)
        return res
    except Exception as e:
        return {"error": str(e)}

#delete transcription given id
@router.delete("/transcription", description="Delete transcription given id")
async def delete_transcription(upload_path: str, db: Session = Depends(get_db)):
    try:
        res = await delete_transcription_path(upload_path, db)
        return res
    except Exception as e:
        return {"error": str(e)}