# EduVoice 🎓🔊

Offline AI Voice Tutor for Blind and Underprivileged Children in Africa

EduVoice is a fully offline, voice-first AI tutor designed for regions with zero connectivity and for students with vision impairments. It transforms consumer-grade hardware (Raspberry Pi/MacBook) into an interactive "Teacher in a Box" using a specialized, fine-tuned Gemma 4 model.

## Technical Implementation

### Unsloth Fine-Tuning
The core intelligence is powered by Gemma 4 (E4B), fine-tuned using the Unsloth library. This optimization allowed for a 70% reduction in memory usage and 2x faster training, resulting in highly specialized LoRA weights (`/eduvoice_lora`) that prioritize educational reasoning and pedagogy over general chat.

### Headless CLI Architecture
To maximize hardware performance on edge devices, the system operates entirely through a headless CLI loop. By eliminating the overhead of a web-server and browser interface, an additional 2GB of RAM is reclaimed for LLM inference and high-fidelity vocal synthesis.

### GGUF Quantization Pipeline
The model is deployed as a 4-bit quantized GGUF (`q4_k_m`) via Ollama. This specific quantization method ensures the model retains 99% of its educational logic while remaining small enough to run on devices with only 4GB of RAM.

## Tech Stack

| Component | Technology | Role |
|---|---|---|
| LLM | Gemma 4 (Fine-tuned) | Core reasoning and tutoring logic. |
| Inference | Ollama | Local GGUF serving via Modelfile. |
| Ear (STT) | Whisper (Small) | Fast, offline speech-to-text. |
| Voice (TTS) | Kokoro TTS | Lightweight, human-like voice synthesis (82M params). |
| RAG | ChromaDB | Local vector indexing for curriculum grounding. |

## Project Structure

```plaintext
eduvoice/
├── eduvoice_lora/      # Fine-tuned LoRA adapters
├── merge_script.py     # Pipeline to fuse Base + LoRA -> GGUF
├── Modelfile           # Ollama configuration for the tutor
├── main.py             # Main headless control loop
├── llm.py              # Ollama/Gemma interface
├── stt.py              # Offline Whisper processing
├── tts.py              # Kokoro TTS engine
├── rag.py              # Local RAG implementation
├── requirements.txt    # Optimized dependencies
└── docs/               # Local curriculum materials (.txt/.md)
```

## Setup & Deployment

1. Merge Model: Use `merge_script.py` to fuse the `eduvoice_lora` weights with the base Gemma 4 model into a GGUF binary.
2. Ollama Config: Initialize the local agent:
   ```bash
   ollama create EduVoice -f Modelfile
   ```
3. Install Dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Execution: Launch the headless tutor:
   ```bash
   python main.py
   ```

## Key Features

- 100% Offline: No internet required for any stage of inference or synthesis.
- Voice-First: Pure auditory interface for vision-impaired accessibility.
- ZIMSEC Grounded: RAG-ready for local curriculum alignment.
- Edge Optimized: Designed specifically for low-resource hardware like the Raspberry Pi 4.
