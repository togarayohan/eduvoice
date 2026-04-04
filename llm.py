import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "gemma4:e4b"

SYSTEM_PROMPT = """You are EduVoice, a friendly and patient AI tutor for children in rural Africa.
You run completely offline on a small device.

STRICT RULES:
- Use PLAIN TEXT ONLY. No markdown, no asterisks, no bold, no bullet symbols, no emojis, no LaTeX, no dollar signs, no backslashes.
- Write in simple spoken English as if talking out loud to a child.
- Keep answers SHORT — 3 to 5 sentences maximum.
- Be warm, encouraging, and easy to understand for ages 6-16.
- Use simple words. Avoid jargon.
- If listing steps, say "First... Then... Finally..." instead of using symbols.
"""

def ask(user_message: str, history: list = []) -> str:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages += history
    messages.append({"role": "user", "content": user_message})

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "messages": messages,
                "stream": False,
                "think": False,
                "options": {
                    "temperature": 0.7,
                    "num_predict": 200,  # shorter = faster
                }
            },
            timeout=120
        )
        response.raise_for_status()
        data = response.json()
        message = data.get("message", {})
        content = message.get("content", "").strip()
        return content

    except requests.exceptions.ConnectionError:
        return "Sorry, I could not connect. Please make sure Ollama is running."
    except requests.exceptions.Timeout:
        return "I took too long to think. Please try again."
    except Exception as e:
        return f"Something went wrong: {str(e)}"


if __name__ == "__main__":
    print("Testing LLM...")
    response = ask("What is the water cycle?")
    print(f"EduVoice: {response}")