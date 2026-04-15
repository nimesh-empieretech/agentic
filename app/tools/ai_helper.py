import google.generativeai as genai
from app.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


def generate_ai_response(role: str, goal: str) -> str:
    prompt = f"""
You are a professional {role} in an enterprise company.

User request:
{goal}

Instructions:
- Give a clear and helpful response
- Be professional and concise
- Ask follow-up questions if needed
- Provide actionable guidance
- Do not mention AI

Response:
"""
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating response: {str(e)}"
