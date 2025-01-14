from fastapi import APIRouter
from src.database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/status")
def health():
    return {"status": "ok"}


    



