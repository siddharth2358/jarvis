from TTS.api import TTS
import uuid
import os

os.makedirs("backend/static", exist_ok=True)

tts = TTS(model_name="tts_models/en/vctk/vits")

def generate_speech(text):
    filename = f"{uuid.uuid4()}.wav"
    filepath = f"backend/static/{filename}"
    tts.tts_to_file(text=text, file_path=filepath)
    return filename
