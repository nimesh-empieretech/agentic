import requests
from app.config import settings

VALID = {"CTO", "COO", "CFO", "HR", "SALES", "GENERAL"}


def smart_route_task(goal: str):
    prompt = f"""
Return ONLY one word from:
CTO, COO, CFO, HR, SALES, GENERAL.

Task: {goal}
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
                "temperature": 0,
            },
        )

        data = response.json()

        print("FULL RESPONSE:", data)

        if "choices" not in data:
            return "GENERAL"

        result = data["choices"][0]["message"]["content"].strip().upper()

        department = result.split()[0].replace(".", "").replace(",", "")

        return department if department in VALID else "GENERAL"

    except Exception as e:
        print("ERROR:", str(e))
        return "GENERAL"
