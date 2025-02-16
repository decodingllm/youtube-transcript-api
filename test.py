import json
#import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app import app

# filepath: /workspaces/youtube-transcript-api/test_app.py

client = TestClient(app)

def test_get_transcript_valid_url():
    valid_url = "https://www.youtube.com/watch?v=Db6ZRMSbUfg"
    response_data = {"transcript_text": "This is a transcript."}

    with patch('utils.get_transcript_with_params') as mock_get_transcript, \
         patch('utils.extract_transcript_text') as mock_extract_transcript:
        
        mock_get_transcript.return_value = json.dumps({"items": []})
        mock_extract_transcript.return_value = response_data["transcript_text"]

        response = client.post("/get_transcript", json={"baseURL": valid_url})
        
        assert response.status_code == 200
        assert response.json() == response_data

def test_get_transcript_invalid_url():
    invalid_url = "https://www.youtube.com/watch?v"

    response = client.post("/get_transcript", json={"baseURL": invalid_url})
    
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid YouTube URL format. Please provide a URL containing video_id starting with '='."}