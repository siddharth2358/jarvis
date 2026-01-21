from faster_whisper import WhisperModel

model = WhisperModel("base", compute_type="int8")

def transcribe_audio(audio_path):
    segments, _ = model.transcribe(audio_path)
    return " ".join(segment.text for segment in segments)
