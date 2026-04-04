import whisper
import sounddevice as sd
import numpy as np
import tempfile
import scipy.io.wavfile as wav
import os

# Use "base" for speed on edge devices, "small" for better accuracy
# On M1 MacBook "small" is still very fast
WHISPER_MODEL = "small"

_model = None

def load_model():
    """Load Whisper model once and cache it."""
    global _model
    if _model is None:
        print(f"Loading Whisper {WHISPER_MODEL} model...")
        _model = whisper.load_model(WHISPER_MODEL)
        print("Whisper ready.")
    return _model


def record_audio(duration: int = 5, sample_rate: int = 16000) -> np.ndarray:
    """
    Record audio from microphone.
    
    Args:
        duration: How many seconds to record
        sample_rate: Audio sample rate (Whisper expects 16kHz)
    
    Returns:
        numpy array of audio samples
    """
    print(f"🎤 Listening for {duration} seconds...")
    audio = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="float32"
    )
    sd.wait()  # Wait until recording is done
    print("✅ Recording complete.")
    return audio.flatten()


def transcribe_audio(audio: np.ndarray, sample_rate: int = 16000) -> str:
    """
    Transcribe numpy audio array to text using Whisper.
    
    Args:
        audio: numpy array of audio samples
        sample_rate: sample rate of the audio
    
    Returns:
        Transcribed text string
    """
    model = load_model()

    # Save to a temp wav file (Whisper needs a file path)
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        tmp_path = f.name
        wav.write(tmp_path, sample_rate, (audio * 32767).astype(np.int16))

    try:
        result = model.transcribe(tmp_path, language="en", fp16=False)
        text = result["text"].strip()
        return text
    finally:
        os.unlink(tmp_path)  # Clean up temp file


def listen(duration: int = 5) -> str:
    """
    High-level function: record from mic and return transcribed text.
    
    Args:
        duration: seconds to listen for
    
    Returns:
        transcribed string
    """
    audio = record_audio(duration=duration)
    text = transcribe_audio(audio)
    print(f"👂 Heard: {text}")
    return text


if __name__ == "__main__":
    print("Testing STT — speak something in the next 5 seconds...")
    result = listen(duration=5)
    print(f"Transcribed: '{result}'")
