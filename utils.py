def extract_transcript_text(apiResponse):
    #print("apiResponse: ", apiResponse)
    transcript_text = []
    if isinstance(apiResponse, dict):
        for key, value in apiResponse.items():
            if key == "text":
                transcript_text.append(value)
            else:
                transcript_text.extend(extract_transcript_text(value))
    elif isinstance(apiResponse, list):
        for item in apiResponse:
            transcript_text.extend(extract_transcript_text(item))
    return transcript_text

def get_transcript_with_params(video_id, api_key, rapidapi_host, platform):
    print("video_id: ", video_id)
    import http.client
    import urllib.parse

    conn = http.client.HTTPSConnection(rapidapi_host)

    headers = {
        'x-rapidapi-key': api_key,
        'x-rapidapi-host': rapidapi_host
    }

    params = {
        'video_id': video_id,
        'platform': platform
    }

    url = "/api/v1/get-transcript-v2?" + urllib.parse.urlencode(params)

    conn.request("GET", url, headers=headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")

from config import tokenizer, model
def summarize_text(text):
    # testing summarization function by getting only the the first 3 sentences
    print("summary function triggered successfully")
    # Tokenize the input text
    inputs = tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=1024, truncation=True)
    
    # Generate summary
    summary_ids = model.generate(inputs, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
    
    # Decode the summary
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    
    return summary