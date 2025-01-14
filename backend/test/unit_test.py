import pytest



def test_upload_audio_file(client):
    with open("test/Test1.mp3", "rb") as audio_file:
        response = client.post("/transcribe", files={"file": ("test.mp3", audio_file, "audio/mp3")})
        assert response.status_code == 200
        assert "transcription" in response.json()

def test_upload_audio_file_invalid(client):
    text_data = b"This is not audio"
    response = client.post(
        "/transcribe",
        files={"file": ("test.txt", text_data, "text/plain")}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Unsupported file type."

def test_search_transcription(client):
    response = client.get("/search", params={"search_term": "non-existant term"})
    assert response.status_code == 200
    assert response.json() == []