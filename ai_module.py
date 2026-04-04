import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

conversation_history = [
    {
        "role": "system",
        "content": (
            "You are Fruit, a helpful friendly personal desktop voice assistant. "
            "You help users control their computer, answer questions, and assist "
            "visually impaired and disabled users. Keep responses short and clear "
            "since they will be spoken aloud."
        )
    }
]

def generate_ai_response(prompt):
    try:
        conversation_history.append({"role": "user", "content": prompt})
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=conversation_history,
            max_tokens=150
        )
        reply = response.choices[0].message.content
        conversation_history.append({"role": "assistant", "content": reply})
        return reply
    except Exception as e:
        print(f"AI Error: {e}")
        return "I had trouble generating a response. Please try again."