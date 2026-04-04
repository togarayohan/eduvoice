import sounddevice as sd
import numpy as np
import re

try:
    from kokoro import KPipeline
    KOKORO_AVAILABLE = True
except ImportError:
    KOKORO_AVAILABLE = False

try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False

_pipeline = None

def clean_text(text: str) -> str:
    """Clean text before speaking — remove emojis, markdown, LaTeX, special characters."""
    # Remove LaTeX math expressions like $\rightarrow$, $x^2$, etc.
    text = re.sub(r'\$[^$]*\$', '', text)
    text = re.sub(r'\\\w+', '', text)  # Remove \rightarrow, \frac, etc.

    # Remove emojis
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"
        u"\U0001F300-\U0001F5FF"
        u"\U0001F680-\U0001F6FF"
        u"\U0001F1E0-\U0001F1FF"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642"
        u"\u2600-\u2B55"
        u"\u200d\u23cf\u23e9\u231a\ufe0f\u3030"
        "]+", flags=re.UNICODE)
    text = emoji_pattern.sub('', text)

    # Remove markdown
    text = re.sub(r'\*+', '', text)
    text = re.sub(r'#+\s*', '', text)
    text = re.sub(r'`+', '', text)
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)  # markdown links

    # Replace arrows and symbols with words
    text = text.replace('→', ' then ').replace('->', ' then ')
    text = text.replace('&', ' and ').replace('%', ' percent ')

    # Clean up whitespace
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\s+', ' ', text)

    return text.strip()


def split_sentences(text: str) -> list:
    """Split text into sentences for streaming TTS."""
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]


def load_kokoro():
    global _pipeline
    if _pipeline is None:
        print("Loading Kokoro TTS...")
        _pipeline = KPipeline(lang_code='a')
        print("Kokoro TTS ready.")
    return _pipeline


def speak_kokoro(text: str, voice: str = "af_heart", speed: float = 0.95):
    pipeline = load_kokoro()
    generator = pipeline(text, voice=voice, speed=speed)
    for _, _, audio in generator:
        if audio is not None:
            sd.play(audio, samplerate=24000)
            sd.wait()


def speak_pyttsx3(text: str):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 0.9)
    engine.say(text)
    engine.runAndWait()


def speak(text: str):
    if not text:
        return

    clean = clean_text(text)
    if not clean:
        return

    print(f"🔊 Speaking: {clean[:80]}{'...' if len(clean) > 80 else ''}")

    if KOKORO_AVAILABLE:
        speak_kokoro(clean)
    elif PYTTSX3_AVAILABLE:
        speak_pyttsx3(clean)
    else:
        print("❌ No TTS engine available.")


if __name__ == "__main__":
    print("Testing TTS with LaTeX cleanup...")
    speak("The water cycle goes like this: $\\rightarrow$ **Evaporation** $\\rightarrow$ **Condensation** (clouds) $\\rightarrow$ **Precipitation** (rain)!")