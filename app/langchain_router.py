import google.generativeai as genai
from app.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")  # ✅ fixed


def smart_route_task(goal: str):
    prompt = f"""
Return ONLY one word from:
CTO, COO, CFO, HR, Sales.

Task: {goal}
"""

    response = model.generate_content(prompt)
    print("FULL RESPONSE:", response)   # 🔥 full object
    print("TEXT:", response.text) 


    return response.text.strip() 
