import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def ask_ai(user_message, history=None):
    messages = [
        {
            "role": "system",
            "content": """You are a professional AI fitness coach.
Format responses clearly using:
- Short headings with emojis
- Bullet points
- Numbered steps if needed
- Keep it structured and readable
- Give practical, science-based advice
- Avoid long paragraphs
- End with a short motivational line."""
        }
    ]

    if history:
        messages.extend(history)

    messages.append({
        "role": "user",
        "content": user_message
    })

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.6,
            max_tokens=1500
        )

        return response.choices[0].message.content

    except Exception as e:
        print("Groq Error:", e)
        return "AI service is temporarily unavailable."
