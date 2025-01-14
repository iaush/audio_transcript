from fastapi import FastAPI
from src.router.health import router as health_router
from src.router.transcript import router as transcript_router
from src.database import Base, init_db
from src.models.transcription import Transcription
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from src.config import settings

UPLOAD_DIR = settings.UPLOAD_DIR

def create_app():
    app = FastAPI()

    app.include_router(health_router, tags=["Health"])
    app.include_router(transcript_router, tags=["Transcribe"])
    init_db()
    app.mount("/src/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")
    return app


app = create_app()


@app.get("/")
def hello_world():
    return {"message": "Hello World!"}

