from fastapi import FastAPI
from src.router.health import router as health_router
from src.router.transcript import router as transcript_router
from src.database import init_db, Base
from src.models.transcription import Transcription

# app = FastAPI()

# app.include_router(health_router, prefix="/health", tags=["Health"])
# app.include_router(transcript_router, tags=["Transcribe"])

# init_db()

def create_app():
    app = FastAPI()

    app.include_router(health_router, prefix="/health", tags=["Health"])
    app.include_router(transcript_router, tags=["Transcribe"])

    init_db()
    return app

app = create_app()

@app.get("/")
def hello_world():
    return {"message": "Hello World!"}

