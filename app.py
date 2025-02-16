from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
from utils import extract_transcript_text, get_transcript_with_params

app = FastAPI()

class URLRequest(BaseModel):
    baseURL: str

@app.post("/get_transcript")
def get_transcript(request: URLRequest):
    baseURL = request.baseURL
    video_id = ""

    if '=' in baseURL:
        parts = baseURL.split('=')
        video_id = parts[1]
    else:
        raise HTTPException(status_code=400, detail="Invalid YouTube URL format. Please provide a URL containing video_id starting with '='.")

    from config import api_key
    rapidapi_host = "youtube-video-summarizer-gpt-ai.p.rapidapi.com"
    platform = "youtube"

    apiResponse = json.loads(get_transcript_with_params(video_id, api_key, rapidapi_host, platform))
    transcript_text = extract_transcript_text(apiResponse)

    return {"transcript_text": transcript_text}
