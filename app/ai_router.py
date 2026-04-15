import google.generativeai as genai
from app.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

VALID_DEPARTMENTS = ["CTO", "COO", "CFO", "HR", "Sales", "GENERAL"]


def smart_route_task(goal: str):
    prompt = f"""
You are a department router.

Return ONLY one word from:
CTO, COO, CFO, HR, Sales, GENERAL

Rules:
- CTO = code, bug, software, website, API, devops, server, database
- COO = operations, workflow, execution, process
- CFO = finance, payment, budget, invoice, salary, accounts
- HR = hiring, leave, employee, attendance, policy
- Sales = leads, clients, proposal, conversion, marketing sales
- GENERAL = greetings, casual chat, unclear tasks, or anything that does not clearly belong to a department

Task: {goal}
"""
    response = model.generate_content(prompt)
    department = response.text.strip().upper()

    if department not in VALID_DEPARTMENTS:
        return "GENERAL"

    return department
