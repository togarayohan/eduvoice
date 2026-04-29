from stt import listen
from llm import ask
from tts import speak

def run_tutor():
    print("--- EduVoice Offline Mode ---")
    # 1. Listen to the student
    user_text = listen(duration=5)
    
    if user_text:
        # 2. Get Socratic response from Ollama
        response = ask(user_text)
        print(f"EduVoice: {response}")
        
        # 3. Speak the response
        speak(response)

if __name__ == "__main__":
    run_tutor()