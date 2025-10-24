print("Week 3 Assignment: Voice Agent Development 😀")

import os
import time

# Import necessary libraries
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import FileResponse

# transcribe audio
from utils.asr import transcribe_audio

# upload dir
UPLOAD_DIR = "uploads/temp"
TRANSCR_DIR = "uploads/audio"
TRANSCR_TEXT_DIR = "uploads/text"
# make sure they exist
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(TRANSCR_DIR, exist_ok=True)
os.makedirs(TRANSCR_TEXT_DIR, exist_ok=True)

app = FastAPI()

@app.post("/chat/")
async def chat_endpoint(request: Request, file: UploadFile = File(...)):
    """
    Accepts audio file and returns audio file.
    """

    # check for only one file.
    form = await request.form()
    if len(form) > 1:
        return {"error": "Only one audio file is allowed per request."}
    
    # save the uploaded file
    audio_bytes = await file.read()

    uploaded_file = os.path.join(UPLOAD_DIR, file.filename)
    with open(uploaded_file, "wb") as f:
        print("Saving uploaded file.🆗")
        f.write(await file.read())

    print("Reading the uploaded file.")

    # TODO: ASR → LLM → TTS

    # transcribe
    some_text = transcribe_audio(audio_bytes=audio_bytes, original_filename=file.filename)
    print(f"\n👌: {some_text}\n")

  
    # Save transcription to a text file using timestamp
    timestamp = time.strftime("%Y%m%d-%H%M%S")  # e.g., 20251024-075230
        
    # Save transcription to a text file
    transcript_path = os.path.join(TRANSCR_TEXT_DIR, f"{timestamp}_{os.path.splitext(file.filename)[0]}_transcript.txt")
    with open(transcript_path, "w") as transcript_file:
        transcript_file.write(some_text)



    # file path 
    # # TODO: Return the actual file.
    # This is a placeholder for testing purposes
    
   
    
    return FileResponse(
        path=uploaded_file, # use the uploaded file as placeholder
        media_type="audio/mpeg",
        filename="test.mp3"
    )