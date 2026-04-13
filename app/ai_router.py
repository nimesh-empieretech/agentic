import google.generativeai as genai
from app.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

VALID_DEPARTMENTS = ["CTO", "COO", "CFO", "HR", "Sales"]


def smart_route_task(goal: str):
    prompt = f"""
Return ONLY one word from:
CTO, COO, CFO, HR, Sales.

Task: {goal}
"""

    response = model.generate_content(prompt)

    department = response.text.strip()

    if department not in VALID_DEPARTMENTS:
        return "COO"

    return department
