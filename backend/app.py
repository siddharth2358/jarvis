from fastapi import FastAPI, UploadFile
from fastapi.staticfiles import StaticFiles
import uuid, shutil

from speech_to_text import transcribe_audio
from text_to_speech import generate_speech
from rag import jarvis_answer
from pinecone_db import store_memory

app = FastAPI()

app.mount("/static", StaticFiles(directory="backend/static"), name="static")

@app.post("/chat")
def chat(message: str):
    response = jarvis_answer(message)
    store_memory(str(uuid.uuid4()), f"Q: {message}\nA: {response}")
    return {"response": response}

@app.post("/voice-chat")
async def voice_chat(audio: UploadFile):
    temp_audio = f"temp_{uuid.uuid4()}.wav"

    with open(temp_audio, "wb") as buffer:
        shutil.copyfileobj(audio.file, buffer)

    text = transcribe_audio(temp_audio)
    response = jarvis_answer(text)
    store_memory(str(uuid.uuid4()), f"Q: {text}\nA: {response}")

    audio_file = generate_speech(response)

    return {
        "text": text,
        "response": response,
        "audio_url": f"/static/{audio_file}"
    }
