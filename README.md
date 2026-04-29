# EduVoice 🎓🔊

**Offline AI Voice Tutor for Blind and Underprivileged Children in Africa**

Built for the [Gemma 4 Good Hackathon (2026)](https://kaggle.com/competitions/gemma-4-good-hackathon)

---

## The Problem
Millions of children across Africa face a massive barrier to education: **Connectivity** and **Accessibility**. 
- **The Internet Gap:** High data costs and unreliable power make cloud-based AI impossible for the majority.
- **The Resource Gap:** Textbooks are scarce; many students rely solely on a teacher's spoken word.
- **The Accessibility Gap:** For blind or vision-impaired children, a lack of internet and a lack of vision equals a total lockout from modern educational tools.

## The Solution
EduVoice is a fully **offline**, **voice-first** AI tutor that transforms a standard PC or Raspberry Pi into a "Teacher in a Box." 

- **Voice-In, Voice-Out:** Zero-screen interface designed specifically for blind students and low-literacy environments.
- **100% Offline:** Runs entirely without internet using a fine-tuned **Gemma 4** model.
- **Curriculum-Grounded:** Uses Local RAG to ensure answers stay within the bounds of ZIMSEC/local school curriculum materials.

---

## Technical Architecture & The "Unsloth" Edge

To make this possible on edge hardware, we utilized a deep optimization stack:

### 1. Fine-tuned with Unsloth (`/eduvoice_lora`)
We optimized **Gemma 4 (E4B)** using **Unsloth** for specialized educational reasoning. The `/eduvoice_lora` folder contains our custom adapters. This process reduced memory usage by 70% and enabled the model to follow complex pedagogical instructions while maintaining a small footprint.

### 2. The Deployment Pipeline (`merge_script.py`)
To bridge the gap between fine-tuning and offline deployment, we implemented a custom GGUF pipeline:
- **Mathematical Merge:** Fuses the base model with our LoRA weights.
- **Quantization (Q4_K_M):** Compresses the model for high-speed performance on **4GB RAM** devices.
- **GGUF Export:** Generates the final binary used by **Ollama** for local inference.

### 3. Headless Architecture
We stripped 100% of the GUI components (no more `web_gui.py`). By removing the browser and web-server overhead, we saved ~2GB of RAM, dedicating every available CPU cycle to inference and vocal synthesis.

---

## ⚠️ Model Download Notice
Due to GitHub's file size limitations (100MB), the final merged **Model.gguf** (approx. 2.4GB) is not hosted directly in this repo.

**To run EduVoice:**
1. **Download:** Get the pre-quantized `Model.gguf` from [INSERT YOUR GOOGLE DRIVE/HF LINK HERE].
2. **Initialize:** Run `ollama create EduVoice -f Modelfile`.
3. **Alternative:** Use the provided `merge_script.py` to regenerate the GGUF using the weights in `/eduvoice_lora`.

---

## Tech Stack

| Component | Technology | Why? |
| :--- | :--- | :--- |
| **Brain (LLM)** | **Gemma 4 (Fine-tuned)** | **Unsloth-optimized**; high reasoning at low memory cost. |
| **Engine** | **Ollama** | Serves the local GGUF via the provided `Modelfile`. |
| **Ear (STT)** | **OpenAI Whisper (Small)** | High-accuracy, offline speech-to-text. |
| **Voice (TTS)** | **Kokoro TTS** | Natural, human-like voice at only 82M parameters. |
| **Memory (RAG)** | **ChromaDB** | Local vector storage for indexing textbooks. |

---

## Project Structure

```text
eduvoice/
├── eduvoice_lora/      # Custom LoRA adapters (Proof of Fine-tuning)
├── Model.gguf          # (Local only) The merged, quantized brain
├── Modelfile           # Ollama configuration for the tutor
├── merge_script.py     # Script to merge LoRA + Base into GGUF
├── main.py             # Headless main loop (Mic -> STT -> LLM -> TTS)
├── llm.py              # Gemma 4 / Ollama interface logic
├── stt.py              # Offline Whisper processing
├── tts.py              # Kokoro text-to-speech engine
├── rag.py              # Local RAG for curriculum grounding
├── requirements.txt    # Optimized dependencies
└── docs/               # Local curriculum files (.txt/.md)
