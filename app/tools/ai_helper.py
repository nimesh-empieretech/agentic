import requests
from app.config import settings


def generate_ai_response(role: str, goal: str) -> str:
    prompt = f"""
You are a professional {role} in an enterprise company.

User message:
{goal}

Instructions:
- Reply naturally and professionally
- Be helpful and practical
- Ask follow-up questions if needed
- Keep the reply clear
- Do not mention AI, model, or system

Response:
"""

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost",
                "X-Title": "agentic-app",
            },
            json={
                "model": "openai/gpt-4o-mini",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
            },
            timeout=30,
        )

        data = response.json()
        print("AI RESPONSE:", data)

        if "choices" not in data:
            return f"Error: {data}"

        return data["choices"][0]["message"]["content"].strip()

    except Exception as e:
        return f"Error generating response: {str(e)}"
