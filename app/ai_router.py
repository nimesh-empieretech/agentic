import google.generativeai as genai
from app.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

VALID_DEPARTMENTS = {"CTO", "COO", "CFO", "HR", "SALES", "GENERAL"}


def smart_route_task(goal: str):
    text = goal.lower().strip()

    # fast keyword routing first
    if any(word in text for word in [
        "hi", "hello", "hii", "hey", "good morning", "good evening"
    ]):
        return "GENERAL"

    if any(word in text for word in [
        "website", "web site", "site", "ecommerce", "portfolio", "landing page",
        "business website", "create website", "new website", "client", "quotation",
        "proposal", "price", "cost", "service"
    ]):
        return "SALES"

    if any(word in text for word in [
        "salary", "invoice", "payment", "budget", "tax", "profit", "expense", "finance"
    ]):
        return "CFO"

    if any(word in text for word in [
        "employee", "leave", "hiring", "interview", "recruitment", "attendance", "hr"
    ]):
        return "HR"

    if any(word in text for word in [
        "workflow", "process", "operations", "coordination", "execution"
    ]):
        return "COO"

    if any(word in text for word in [
        "bug", "error", "fix", "code", "api", "backend", "frontend", "database",
        "server", "deployment", "devops", "infra", "infrastructure", "react",
        "python", "fastapi", "node", "login issue"
    ]):
        return "CTO"

    # Gemini routing fallback
    prompt = f"""
You are a department router.

Return ONLY one word from:
CTO
COO
CFO
HR
SALES
GENERAL

Rules:
- CTO = code, bug, API, software, website development technical issues, app, database, server, deployment
- COO = operations, workflow, execution, process
- CFO = finance, budget, invoice, payment, tax
- HR = hiring, leave, employee, interview, recruitment
- SALES = service inquiry, new project, new website, app development inquiry, proposal, cost, client discussion
- GENERAL = greetings, casual chat, unclear message

Message: {goal}
"""

    try:
        response = model.generate_content(prompt)
        raw = (getattr(response, "text", "") or "").strip().upper()
        department = raw.split()[0].replace(".", "").replace(",", "") if raw else "GENERAL"

        if department not in VALID_DEPARTMENTS:
            return "GENERAL"

        return department
    except Exception:
        return "GENERAL"