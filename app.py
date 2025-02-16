print("Loading app.py")
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
from utils import extract_transcript_text, get_transcript_with_params

app = FastAPI()
print("app.py loaded")

class URLRequest(BaseModel):
    baseURL: str

print("URLRequest class defined")
@app.post("/get_transcript")
def get_transcript(request: URLRequest):
    baseURL = request.baseURL
    video_id = ""
    print("baseURL: ", baseURL)

    if '=' in baseURL:
        print("baseURL: ", baseURL)
        parts = baseURL.split('=')
        video_id = parts[1]
        print("video_id: ", video_id)
    else:
        raise HTTPException(status_code=400, detail="Invalid YouTube URL format. Please provide a URL containing video_id starting with '='.")

    from config import api_key
    from config import rapidapi_host
    platform = "youtube"

    apiResponse = json.loads(get_transcript_with_params(video_id, api_key, rapidapi_host, platform))
    transcript_text = extract_transcript_text(apiResponse)

    return {"transcript_text": transcript_text}

#get_transcript(request=URLRequest(baseURL="https://www.youtube.com/watch?v=Db6ZRMSbUfg"))
#get_transcript({"baseURL": "https://www.youtube.com/watch?v=Db6ZRMSbUfg"})