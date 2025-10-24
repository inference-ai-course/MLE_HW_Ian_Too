import os
import time
import logging

# Import necessary libraries
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import FileResponse



# transcribe audio
from utils.asr import transcribe_audio

# llm response
from utils.response_gen import generate_response, generate_response_ollama

# upload dir
UPLOAD_DIR = "uploads/temp"
TRANSCR_DIR = "uploads/audio"
TRANSCR_TEXT_DIR = "uploads/text"
# make sure they exist
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(TRANSCR_DIR, exist_ok=True)
os.makedirs(TRANSCR_TEXT_DIR, exist_ok=True)

app = FastAPI()

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logging.info("Week 3 Assignment: Voice Agent Development 😀")

@app.post("/chat/")
async def chat_endpoint(request: Request, file: UploadFile = File(...)):
    """
    Accepts audio file and returns audio file.
    """

    # check for only one file.
    form = await request.form()
    if len(form) > 1:
        logging.warning("Only one audio file is allowed per request.")
        return {"error": "Only one audio file is allowed per request."}
    
    # save the uploaded file
    audio_bytes = await file.read()

    uploaded_file = os.path.join(UPLOAD_DIR, file.filename)
    with open(uploaded_file, "wb") as f:
        logging.info("Saving uploaded file.🆗")
        f.write(await file.read())

    logging.debug("Reading the uploaded file.")

    # TODO: ASR → LLM → TTS

    # transcribe
    user_instruction_text = transcribe_audio(audio_bytes=audio_bytes, original_filename=file.filename)
    logging.debug(f"\n👌: {user_instruction_text}\n")

    # Save transcription to a text file using timestamp
    timestamp = time.strftime("%Y%m%d-%H%M%S")  # e.g., 20251024-075230
        
    # Save transcription to a text file
    transcript_path = os.path.join(TRANSCR_TEXT_DIR, f"{timestamp}_{os.path.splitext(file.filename)[0]}_transcript.txt")
    with open(transcript_path, "w") as transcript_file:
        transcript_file.write(user_instruction_text)
    
    # get respinse from llm
    llm_response = generate_response_ollama(user_instruction_text)
    logging.debug(f"\nLlm Response:\n{llm_response}\n")

    # text to speech

    # file path 
    # # TODO: Return the actual file.
    # This is a placeholder for testing purposes
    return FileResponse(
        path=uploaded_file, # use the uploaded file as placeholder
        media_type="audio/mpeg",
        filename="test.mp3"
    )


# test
#logging.debug(f"{generate_response('Hello there, what is your name?')}")
#logging.debug(f"{generate_response_ollama('Hello there, what is your name?')}")
#logging.debug(f"{generate_response_ollama('Can we go home together?')}")
#logging.debug(f"{generate_response_ollama('Remind me your name again? I am Ian Too')}")
