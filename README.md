# EduVoice 🎓🔊

**Offline AI Voice Tutor for Blind and Underprivileged Children in Africa**

Built for the [Gemma 4 Good Hackathon (2026)](https://kaggle.com/competitions/gemma-4-good-hackathon)

---

## The Problem

Millions of children across Africa face a massive barrier to education: **Connectivity** and **Accessibility**. 
- **The Internet Gap:** High data costs and unreliable power make cloud-based AI impossible for the majority.
- **The Resource Gap:** Textbooks are scarce; many students rely solely on a teacher's spoken word.
- **The Accessibility Gap:** For blind or vision-impaired children, a lack of internet and lack of vision equals a total lockout from modern educational tools.

## The Solution

EduVoice is a fully **offline**, **voice-first** AI tutor that transforms a standard PC or Raspberry Pi into a "Teacher in a Box." 

- **Voice-In, Voice-Out:** Zero-screen interface designed specifically for blind students and low-literacy environments.
- **100% Offline:** Runs entirely without internet using a fine-tuned **Gemma 4** model.
- **Curriculum-Grounded:** Uses Local RAG to ensure answers stay within the bounds of actual school curriculum materials.

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

```text
eduvoice/
├── eduvoice_lora/      # Custom LoRA adapters (Fine-tuning weights)
├── Model.gguf          # The merged, quantized brain (Ready for PC/Pi)
├── Modelfile           # Ollama configuration for the tutor
├── merge_script.py     # Script to merge LoRA + Base into GGUF
├── main.py             # Headless main loop (Mic -> STT -> LLM -> TTS -> Speaker)
├── llm.py              # Gemma 4 / Ollama interface logic
├── stt.py              # Offline Whisper processing
├── tts.py              # Kokoro text-to-speech engine
├── rag.py              # Local RAG for curriculum grounding
├── requirements.txt    # Optimized dependencies for headless PC/Pi
└── docs/               # Folder for local curriculum .txt/.md files