import requests
from app.config import settings

VALID_DEPARTMENTS = {"CTO", "COO", "CFO", "HR", "SALES", "GENERAL"}


def smart_route_task(goal: str) -> str:
    text = goal.lower().strip()

    if any(
        word in text
        for word in ["hi", "hello", "hii", "hey", "good morning", "good evening"]
    ):
        return "GENERAL"

    if any(
        word in text
        for word in [
            "bug",
            "error",
            "fix",
            "code",
            "api",
            "backend",
            "frontend",
            "database",
            "server",
            "deployment",
            "devops",
            "react",
            "python",
            "fastapi",
            "node",
            "login issue",
            "technical issue",
            "website issue",
            "app issue",
        ]
    ):
        return "CTO"

    if any(
        word in text
        for word in [
            "quotation",
            "proposal",
            "price",
            "cost",
            "service",
            "need website",
            "new website",
            "new project",
            "client",
            "business website",
            "create website",
            "website development",
            "app development",
        ]
    ):
        return "SALES"

    if any(
        word in text
        for word in [
            "salary",
            "invoice",
            "payment",
            "budget",
            "tax",
            "profit",
            "expense",
            "finance",
        ]
    ):
        return "CFO"

    if any(
        word in text
        for word in [
            "employee",
            "leave",
            "hiring",
            "interview",
            "recruitment",
            "attendance",
            "hr",
        ]
    ):
        return "HR"

    if any(
        word in text
        for word in ["workflow", "process", "operations", "coordination", "execution"]
    ):
        return "COO"

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
- CTO = code, bug, API, software, website technical issues, app, database, server, deployment
- COO = operations, workflow, execution, process
- CFO = finance, budget, invoice, payment, tax
- HR = hiring, leave, employee, interview, recruitment
- SALES = service inquiry, new project, website/app development inquiry, proposal, cost, client discussion
- GENERAL = greetings, casual chat, unclear message

Message: {goal}
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
            timeout=30,
        )

        data = response.json()
        print("ROUTER RESPONSE:", data)

        if "choices" not in data:
            return "GENERAL"

        raw = data["choices"][0]["message"]["content"].strip().upper()
        department = (
            raw.split()[0].replace(".", "").replace(",", "") if raw else "GENERAL"
        )

        return department if department in VALID_DEPARTMENTS else "GENERAL"

    except Exception as e:
        print("Routing error:", str(e))
        return "GENERAL"


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
                "temperature": 0.7,
            },
            timeout=30,
        )

        data = response.json()
        print("AI RESPONSE:", data)

        if "choices" not in data:
            return f"Error generating response: {data}"

        content = data["choices"][0]["message"]["content"].strip()
        return content if content else "Sorry, I could not generate a proper response."

    except Exception as e:
        return f"Error generating response: {str(e)}"
