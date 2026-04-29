import requests
import re

OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
MODEL = "eduvoice"

def ask(prompt, history=None):
    # If history is passed, you can append it to messages, 
    # but for a quick fix, just accept the argument:
    messages = [{"role": "user", "content": prompt}]
    
    payload = {
        "model": MODEL,
        "messages": messages,
        "stream": False
    }
    # ... rest of your code ...
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        raw_content = response.json().get("message", {}).get("content", "")

        # 1. Look for the common "done thinking" or "Final Output" markers
        # We use re.split with IGNORECASE to catch variations
        markers = [r"done thinking\.", r"Final Output Generation\.", r"Final Output:"]
        pattern = "|".join(markers)
        
        parts = re.split(pattern, raw_content, flags=re.IGNORECASE)
        
        # If a marker was found, the actual answer is the last part
        if len(parts) > 1:
            clean_content = parts[-1].strip()
        else:
            # 2. Fallback: If no markers, take the last double-newline block 
            # (Thinking blocks are usually separated by whitespace)
            blocks = [p for p in raw_content.split('\n\n') if p.strip()]
            clean_content = blocks[-1].strip() if blocks else raw_content

        return clean_content

    except Exception as e:
        return f"Error connecting to Brain: {e}"

if __name__ == "__main__":
    # Test the filter
    test_q = "What is a star?"
    print(f"Student: {test_q}")
    print(f"EduVoice: {ask(test_q)}")