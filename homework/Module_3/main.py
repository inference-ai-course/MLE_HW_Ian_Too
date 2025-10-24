print("Week 3 Assignment: Voice Agent Development 😀")

import os

# Import necessary libraries
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse

# transcribe audio
from utils.asr import transcribe_audio

# upload dir
UPLOAD_DIR = "uploads/temp"
TRANSCR_DIR = "uploads/audio"
# make sure they exist
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(TRANSCR_DIR, exist_ok=True)

app = FastAPI()

@app.post("/chat/")
async def chat_endpoint(file: UploadFile = File(...)):
    """
    Accepts audio file and returns audio file.
    """

    # save the uploaded file
    uploaded_file = os.path.join(UPLOAD_DIR, file.filename)
    with open(uploaded_file, "wb") as f:
        print("Saving uploaded file.🆗")
        f.write(await file.read())

    # read the uploaded file
    with open(uploaded_file, "rb") as f:
        print("Reading the uploaded file.")
        audio_bytes = file.read()

    # TODO: ASR → LLM → TTS

    # asr
    some_text = transcribe_audio(audio_bytes=audio_bytes)
    print(f"👌: {some_text}")

    # file path 
    # # TODO: Return the actual file.
    # This is a placeholder for testing purposes
    file_path = "test_data/audio/sample-0.mp3"
   
    
    return FileResponse(
        path=file_path,
        media_type="audio/mpeg",
        filename="test.mp3"
    )