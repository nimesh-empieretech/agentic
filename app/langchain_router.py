import json
import requests
from app.config import settings

VALID = {"CTO", "COO", "CFO", "HR", "SALES", "GENERAL"}


def smart_route_task(goal: str):
    text = goal.lower().strip()

    if "open whatsapp" in text or text == "whatsapp":
        return {
            "department": "GENERAL",
            "message": "Opening WhatsApp",
            "action": "open_app",
            "app": "whatsapp",
            "url": "919999999999",
        }

    if "open youtube" in text or text == "youtube":
        return {
            "department": "GENERAL",
            "message": "Opening YouTube",
            "action": "open_app",
            "app": "youtube",
            "url": "https://youtu.be/dQw4w9WgXcQ",
        }

    if "call" in text or "dial" in text:
        return {
            "department": "GENERAL",
            "message": "Opening dialer",
            "action": "open_app",
            "app": "phone",
            "url": "919999999999",
        }

    if "sms" in text or "message" in text:
        return {
            "department": "GENERAL",
            "message": "Opening messages",
            "action": "open_app",
            "app": "sms",
            "url": "919999999999",
        }

    if "email" in text or "mail" in text:
        return {
            "department": "GENERAL",
            "message": "Opening email",
            "action": "open_app",
            "app": "email",
            "url": "test@gmail.com",
        }

    prompt = f"""
Return ONLY valid JSON in this format:
{{
  "department": "CTO|COO|CFO|HR|SALES|GENERAL",
  "message": "short reply",
  "action": "none|open_app",
  "app": "youtube|whatsapp|phone|sms|email|browser|null",
  "url": "optional value"
}}

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
