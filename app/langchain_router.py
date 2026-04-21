import json
import requests
from app.config import settings

VALID = {"CTO", "COO", "CFO", "HR", "SALES", "GENERAL"}


def smart_route_task(goal: str):
    prompt = f"""
Return ONLY valid JSON in this format:
{{
  "department": "CTO|COO|CFO|HR|SALES|GENERAL",
  "message": "short reply",
  "action": "none|open_app",
  "app": "youtube|whatsapp|phone|sms|email|browser|null",
  "url": "optional value"
}}

Examples:
- Open YouTube -> {{"department":"GENERAL","message":"Opening YouTube","action":"open_app","app":"youtube","url":"https://youtu.be/dQw4w9WgXcQ"}}
- Open WhatsApp -> {{"department":"GENERAL","message":"Opening WhatsApp","action":"open_app","app":"whatsapp","url":"919999999999"}}
- Call someone -> {{"department":"GENERAL","message":"Opening dialer","action":"open_app","app":"phone","url":"919999999999"}}
- Send SMS -> {{"department":"GENERAL","message":"Opening messages","action":"open_app","app":"sms","url":"919999999999"}}
- Send email -> {{"department":"GENERAL","message":"Opening email","action":"open_app","app":"email","url":"test@gmail.com"}}
- Open website -> {{"department":"GENERAL","message":"Opening browser","action":"open_app","app":"browser","url":"https://google.com"}}

Task: {goal}
"""

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost",
                "X-Title": "agentic-app",
            },
            json={
                "model": "openai/gpt-4o-mini",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0,
            },
            timeout=30,
        )

        response.raise_for_status()
        data = response.json()

        if "choices" not in data or not data["choices"]:
            return {
                "department": "GENERAL",
                "message": "No valid response",
                "action": "none",
                "app": None,
                "url": None,
            }

        content = data["choices"][0].get("message", {}).get("content", "").strip()
        parsed = json.loads(content)

        department = str(parsed.get("department", "GENERAL")).upper().strip()
        parsed["department"] = department if department in VALID else "GENERAL"

        parsed.setdefault("message", "")
        parsed.setdefault("action", "none")
        parsed.setdefault("app", None)
        parsed.setdefault("url", None)

        return parsed

    except Exception as e:
        return {
            "department": "GENERAL",
            "message": str(e),
            "action": "none",
            "app": None,
            "url": None,
        }
