import http.client
import urllib.parse
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document


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

def get_transcript_with_params(video_id):
    print("video_id: ", video_id)

    from config import api_key
    from config import rapidapi_host
    platform = "youtube"

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

def text_summarisation(transcript_text):
    print("text_summarisation function triggered successfully")
    
    from config import api_key
    from config import gpt_rapidapi_host

    conn = http.client.HTTPSConnection(gpt_rapidapi_host)

    headers = {
        'x-rapidapi-key': api_key,
        'x-rapidapi-host': gpt_rapidapi_host,
        'Content-Type': "application/json"
    }

    conn.request("POST", "/summarize", transcript_text, headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")
    

def text_summarisation_siddharth(transcript_text):

    api_key = "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"

    # Initialize the OpenAI LLM
    llm = ChatGroq(api_key=api_key)

    # Initialize the text splitter
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

    # Create a Document object from the transcript text
    docs = [Document(page_content=transcript_text[0:5000])]
    try:
        # Split text into chunks
        chunks = text_splitter.split_documents(docs)

        prompt_template = """Write a concise summary of the following:
        {text}
        CONCISE SUMMARY:"""
        prompt = PromptTemplate(template=prompt_template,input_variables=["text"])

        refine_template = (
        "Your job is to produce a final summary\n"
        "We have provided an existing summary up to a certain point: {existing_answer}\n"
        "We have the opportunity to refine the existing summary"
        "(only if needed) with some more context below.\n"
        "------------\n"
        "{text}\n"
        "------------\n"
        "If the context isn't useful, return the original summary."
        )
        refine_prompt = PromptTemplate(template=refine_template,input_variables=["existing_answer","text"])
        chain = load_summarize_chain(
            llm=llm,
            chain_type="refine",
            question_prompt=prompt,
            refine_prompt=refine_prompt,
            return_intermediate_steps=True,
            input_key="input_documents",
            output_key="output_text",
        )
        # result = chain({"input_documents": chunks}, return_only_outputs=True)
        result = chain.invoke({"input_documents":chunks})
        return result["output_text"]
        
    except Exception as e:
        return f"Error: {str(e)}"


    # print("text_summarisation function triggered successfully")
    
    # from config import api_key
    # from config import gpt_rapidapi_host
    # conn = http.client.HTTPSConnection(gpt_rapidapi_host)

    # headers = {
    #     'x-rapidapi-key': api_key,
    #     'x-rapidapi-host': gpt_rapidapi_host,
    #     'Content-Type': "application/json"
    # }

    # conn.request("POST", "/summarize", transcript_text, headers)
    # res = conn.getresponse()
    # data = res.read()
    # return data.decode("utf-8")

#from config import tokenizer, model
#def summarize_text(text):
    # testing summarization function by getting only the the first 3 sentences
    print("summary function triggered successfully")
    # Tokenize the input text
    #inputs = tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=1024, truncation=True)
    
    # Generate summary
   # summary_ids = model.generate(inputs, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
    
    # Decode the summary
    #summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    
   # return summary