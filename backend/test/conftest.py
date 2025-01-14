import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from src.database import Base, get_db
from src.main import create_app
from src.models.transcription import Transcription

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

@pytest.fixture(scope="function")
def db_session():
    
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Create all tables before tests
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()
    try:
        yield session  
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)  # Drop tables after tests

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session  # Use the session provided by db_session
        finally:
            pass  
    app = create_app()
    app.dependency_overrides[get_db] = override_get_db  
    with TestClient(app) as test_client:
        yield test_client  # Provide the TestClient to tests
    app.dependency_overrides.clear()