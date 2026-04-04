"""
EduVoice — Offline AI Voice Tutor for Children
================================================
Built for the Gemma 4 Good Hackathon

Powered by:
- Gemma 4 (gemma4:e4b) via Ollama — fully offline LLM
- Whisper (small) — offline speech-to-text
- Kokoro TTS — offline text-to-speech
- ChromaDB + SentenceTransformers — local RAG over curriculum docs

Usage:
    python main.py              # voice mode (default)
    python main.py --text       # text mode (for testing without mic)
    python main.py --index      # re-index curriculum documents
"""
import os
os.environ["TRANSFORMERS_OFFLINE"] = "1"
os.environ["HF_DATASETS_OFFLINE"] = "1"
os.environ["HF_HUB_OFFLINE"] = "1"

import argparse
import sys
from llm import ask
from tts import speak
from rag import augment_prompt, index_documents

# Conversation history for multi-turn memory (kept short to save RAM)
MAX_HISTORY = 6  # last 3 exchanges

def run_voice_mode():
    """Main loop in voice mode — child speaks, EduVoice responds."""
    from stt import listen
    
    speak("Hello! I am EduVoice, your learning assistant. I am here to help you learn. What would you like to know today?")
    
    history = []
    
    print("\n🟢 EduVoice is running. Press Ctrl+C to exit.\n")
    
    while True:
        try:
            # Listen for child's question
            print("\n--- Listening (5 seconds) ---")
            user_input = listen(duration=5)
            
            if not user_input or len(user_input.strip()) < 2:
                speak("I did not hear anything. Please try again.")
                continue
            
            print(f"Child: {user_input}")
            
            # Check for exit commands
            if any(word in user_input.lower() for word in ["goodbye", "bye", "stop", "exit", "quit"]):
                speak("Goodbye! Keep learning and never stop asking questions!")
                break
            
            # Augment with curriculum context if available
            augmented = augment_prompt(user_input)
            
            # Get response from Gemma 4
            print("EduVoice is thinking... 🤔")
            response = ask(augmented, history=history)
            
            if not response:
                response = "I am not sure about that. Can you try asking in a different way?"
            
            print(f"EduVoice: {response}")
            
            # Speak the response
            speak(response)
            
            # Update conversation history
            history.append({"role": "user", "content": user_input})
            history.append({"role": "assistant", "content": response})
            
            # Keep history manageable
            if len(history) > MAX_HISTORY:
                history = history[-MAX_HISTORY:]
        
        except KeyboardInterrupt:
            print("\n\nShutting down EduVoice...")
            speak("Goodbye! Keep learning!")
            break
        except Exception as e:
            print(f"Error: {e}")
            speak("Sorry, something went wrong. Let us try again.")


def run_text_mode():
    """Text-only mode for testing without microphone."""
    from tts import speak
    
    speak("Hello! EduVoice text mode is active. Type your questions below.")
    
    history = []
    
    print("\n🟢 EduVoice TEXT MODE. Type 'quit' to exit.\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ["quit", "exit", "bye", "goodbye"]:
                speak("Goodbye! Keep learning!")
                break
            
            # Augment with curriculum context
            augmented = augment_prompt(user_input)
            
            # Get response
            print("EduVoice is thinking... 🤔")
            response = ask(augmented, history=history)
            
            if not response:
                response = "I am not sure about that. Can you try asking in a different way?"
            
            print(f"\nEduVoice: {response}\n")
            
            # Speak it too
            speak(response)
            
            # Update history
            history.append({"role": "user", "content": user_input})
            history.append({"role": "assistant", "content": response})
            
            if len(history) > MAX_HISTORY:
                history = history[-MAX_HISTORY:]
        
        except KeyboardInterrupt:
            print("\nShutting down...")
            speak("Goodbye!")
            break


def main():
    parser = argparse.ArgumentParser(description="EduVoice — Offline AI Tutor")
    parser.add_argument("--text", action="store_true", help="Run in text mode (no mic)")
    parser.add_argument("--index", action="store_true", help="Index curriculum documents and exit")
    args = parser.parse_args()
    
    if args.index:
        print("Indexing curriculum documents...")
        index_documents()
        print("Done.")
        return
    
    print("""
    ╔══════════════════════════════════════╗
    ║         EduVoice v1.0                ║
    ║   Offline AI Tutor for Children      ║
    ║   Powered by Gemma 4 + Ollama        ║
    ╚══════════════════════════════════════╝
    """)
    
    if args.text:
        run_text_mode()
    else:
        run_voice_mode()


if __name__ == "__main__":
    main()