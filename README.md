# EduVoice 🎓🔊

**Offline AI Voice Tutor for Blind and Underprivileged Children in Africa**

Built for the [Gemma 4 Good Hackathon](https://kaggle.com/competitions/gemma-4-good-hackathon)

---

## The Problem

Millions of children across rural Africa have no reliable internet access, no access to quality teachers, and — for blind children — no accessible learning tools at all. A child who cannot see and cannot access the internet is effectively locked out of education.

## The Solution

EduVoice is a fully **offline**, **voice-first** AI tutor that runs on low-cost hardware (Raspberry Pi or any laptop). A child simply speaks their question and EduVoice responds with a clear, friendly spoken answer — grounded in real curriculum materials.

No internet. No screen. No barriers.

---

## Tech Stack

| Component | Technology | Why |
|-----------|-----------|-----|
| LLM | Gemma 4 (gemma4:e4b) via Ollama | Offline, edge-optimized, fast on M1/Pi |
| Speech-to-Text | Whisper (small) | Offline, accurate, runs on CPU |
| Text-to-Speech | Kokoro TTS | Natural voice, fully offline |
| RAG | ChromaDB + SentenceTransformers | Local curriculum grounding |

---

## Setup

### 1. Install Ollama and pull Gemma 4
```bash
# Install Ollama from https://ollama.com
ollama pull gemma4:e4b
```

### 2. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 3. Add curriculum documents
Place `.txt` or `.md` curriculum files in the `docs/` folder, then index them:
```bash
python main.py --index
```

### 4. Run EduVoice
```bash
# Voice mode (default)
python main.py

# Text mode (for testing)
python main.py --text
```

---

## Project Structure

```
eduvoice/
├── main.py          # Entry point and main loop
├── llm.py           # Gemma 4 via Ollama
├── stt.py           # Whisper speech-to-text
├── tts.py           # Kokoro text-to-speech
├── rag.py           # Local RAG over curriculum docs
├── requirements.txt
└── docs/            # Add your curriculum .txt/.md files here
```

---

## Hardware Targets

- **Development**: MacBook M1 (16GB RAM)
- **Deployment**: Raspberry Pi 4 (4GB RAM) — the EduVoice Kit

---

## Roadmap

- [ ] Shona language support
- [ ] Ndebele language support  
- [ ] Wake word detection ("Hey EduVoice")
- [ ] Fine-tuned model on African curriculum (Unsloth)
- [ ] Raspberry Pi deployment kit
- [ ] Solar-powered enclosure design
