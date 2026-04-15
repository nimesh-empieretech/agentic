import google.generativeai as genai
from app.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


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
- If the user greets, reply politely
- If the user asks for a service, explain the next steps

Response:
"""
    try:
        response = model.generate_content(prompt)
        text = getattr(response, "text", "") or ""
        return text.strip() if text.strip() else "Sorry, I could not generate a proper response."
    except Exception as e:
        return f"Error generating response: {str(e)}"