import google.generativeai as genai
from app.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

VALID_DEPARTMENTS = {"CTO", "COO", "CFO", "HR", "SALES", "GENERAL"}


def smart_route_task(goal: str):
    prompt = f"""
You are a department router for an enterprise AI system.

Return ONLY one word from this list:
CTO
COO
CFO
HR
SALES
GENERAL

Routing rules:
- CTO = code, bug, API, software, website, app, database, server, devops, deployment, infrastructure
- COO = operations, execution, workflow, business process, internal coordination
- CFO = finance, accounts, invoice, salary, payment, budget, tax, profit, expense
- HR = hiring, interview, leave, attendance, employee issues, payroll policy, recruitment
- SALES = leads, prospects, client follow-up, conversion, proposal, sales pitch, deal closing
- GENERAL = greetings, casual chat, unclear requests, or anything that does not clearly fit above

Task: {goal}
"""

    try:
        response = model.generate_content(prompt)

        raw_text = (response.text or "").strip().upper()
        print("FULL RESPONSE:", response)
        print("TEXT:", raw_text)

        department = raw_text.split()[0].replace(".", "").replace(",", "")

        if department not in VALID_DEPARTMENTS:
            return "GENERAL"

        return department

    except Exception as e:
        print("Router error:", e)
        return "GENERAL"