import whisper
import sounddevice as sd
import numpy as np
import tempfile
import scipy.io.wavfile as wav
import os

# Add this to stt.py
def transcribe_file(file_path):
    model = load_model() # Uses your pre-loaded global model
    result = model.transcribe(file_path, language="en", fp16=False)
    return result["text"].strip()

# Configuration
WHISPER_MODEL_NAME = "small"

# Pre-load the model globally so it doesn't reload on every turn
print(f"Loading Whisper {WHISPER_MODEL_NAME}...")
_model = whisper.load_model(WHISPER_MODEL_NAME)
print("Whisper ready.")

def record_audio(duration=5, sample_rate=16000):
    """Records audio from the microphone."""
    print(f"🎤 Listening for {duration} seconds...")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype="float32")
    sd.wait()
    return audio.flatten()

def transcribe_audio(audio, sample_rate=16000):
    """Transcribes the audio array using the global model."""
    if np.max(np.abs(audio)) < 0.01: # Silence threshold
        return ""

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        tmp_path = f.name
        wav.write(tmp_path, sample_rate, (audio * 32767).astype(np.int16))

    try:
        result = _model.transcribe(tmp_path, language="en", fp16=False)
        return result["text"].strip()
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)

def listen(duration=5):
    """The function main.py is looking for."""
    audio = record_audio(duration=duration)
    text = transcribe_audio(audio)
    print(f"👂 Heard: {text}")
    return text

if __name__ == "__main__":
    # Test solo
    print(listen())