#api_key & hostname for the YouTube API
api_key = "2bd75d2069msh7d63312ea77e344p1786cbjsn875221b51434"
rapidapi_host = "youtube-video-summarizer-gpt-ai.p.rapidapi.com"

#loading Bart model and tokenizer
from transformers import BartForConditionalGeneration, BartTokenizer
summary_model = "facebook/bart-large-cnn"
tokenizer = BartTokenizer.from_pretrained(summary_model)
model = BartForConditionalGeneration.from_pretrained(summary_model)