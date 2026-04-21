from typing import Literal, Optional

from pydantic import BaseModel, Field

from langchain_openrouter import ChatOpenRouter
from langchain_core.prompts import ChatPromptTemplate

from app.config import settings


VALID_DEPARTMENTS = {"CTO", "COO", "CFO", "HR", "SALES", "GENERAL"}


class RouteDecision(BaseModel):
    department: Literal["CTO", "COO", "CFO", "HR", "SALES", "GENERAL"] = Field(
        default="GENERAL"
    )
    message: str = Field(default="")
    action: Literal["none", "open_app"] = Field(default="none")
    app: Optional[
        Literal["youtube", "whatsapp", "phone", "sms", "email", "browser"]
    ] = Field(default=None)
    url: Optional[str] = Field(default=None)


def _get_router_llm() -> ChatOpenRouter:
    return ChatOpenRouter(
        model="openai/gpt-4o-mini",
        api_key=settings.OPENROUTER_API_KEY,
        temperature=0,
        max_retries=2,
        default_headers={
            "HTTP-Referer": "http://localhost",
            "X-Title": "agentic-app",
        },
    )


def _rule_based_route(goal: str) -> Optional[RouteDecision]:
    text = goal.lower().strip()

    if not text:
        return RouteDecision(
            department="GENERAL",
            message="Please enter a message.",
            action="none",
        )

    greetings = ["hi", "hello", "hii", "hey", "good morning", "good evening"]
    if any(word in text for word in greetings):
        return RouteDecision(
            department="GENERAL",
            message="Hello! How can I help you today?",
            action="none",
        )

    if "open whatsapp" in text or "whatsapp" in text:
        return RouteDecision(
            department="GENERAL",
            message="Opening WhatsApp",
            action="open_app",
            app="whatsapp",
            url="919999999999",
        )

    if "open youtube" in text or "youtube" in text:
        return RouteDecision(
            department="GENERAL",
            message="Opening YouTube",
            action="open_app",
            app="youtube",
            url="https://youtu.be/dQw4w9WgXcQ",
        )

    if "call" in text or "dial" in text:
        return RouteDecision(
            department="GENERAL",
            message="Opening dialer",
            action="open_app",
            app="phone",
            url="917359208957",
        )

    if "sms" in text or "message" in text:
        return RouteDecision(
            department="GENERAL",
            message="Opening messages",
            action="open_app",
            app="sms",
            url="917359208957",
        )

    if "email" in text or "mail" in text:
        return RouteDecision(
            department="GENERAL",
            message="Opening email",
            action="open_app",
            app="email",
            url="nimesh.empieretech15@gmail.com",
        )

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
        return RouteDecision(
            department="CTO",
            message="Routing to CTO team",
            action="none",
        )

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
        return RouteDecision(
            department="SALES",
            message="Routing to Sales team",
            action="none",
        )

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
        return RouteDecision(
            department="CFO",
            message="Routing to Finance team",
            action="none",
        )

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
        return RouteDecision(
            department="HR",
            message="Routing to HR team",
            action="none",
        )

    if any(
        word in text
        for word in ["workflow", "process", "operations", "coordination", "execution"]
    ):
        return RouteDecision(
            department="COO",
            message="Routing to Operations team",
            action="none",
        )

    return None


def smart_route_task(goal: str) -> dict:
    """
    Returns:
    {
        "department": "CTO|COO|CFO|HR|SALES|GENERAL",
        "message": "short reply",
        "action": "none|open_app",
        "app": "youtube|whatsapp|phone|sms|email|browser|null",
        "url": "optional value"
    }
    """
    rule_result = _rule_based_route(goal)
    if rule_result:
        return rule_result.model_dump()

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
You are a strict enterprise router.

Return structured output only.

Department rules:
- CTO = code, bugs, APIs, backend, frontend, database, server, deployment, DevOps, technical issues
- COO = workflow, operations, execution, coordination, process
- CFO = finance, invoice, payment, budget, tax, salary, expense, profit
- HR = hiring, leave, employee, recruitment, interview, attendance
- SALES = proposal, quotation, pricing, new project, client discussion, website/app service inquiry
- GENERAL = greetings, casual chat, unclear requests, app opening requests

Action rules:
- Use action="open_app" only if the user explicitly wants to open an app/site.
- Otherwise action="none".

App rules:
- whatsapp -> use when user asks to open WhatsApp
- youtube -> use when user asks to open YouTube
- phone -> use when user asks to call/dial
- sms -> use when user asks to send/open messages
- email -> use when user asks to open email
- browser -> use when user asks to open a website

If action="none", set app=null and url=null.
If action="open_app", fill app and url clearly.

Keep message short.
""",
            ),
            ("human", "Message: {goal}"),
        ]
    )

    try:
        llm = _get_router_llm()
        structured_llm = llm.with_structured_output(RouteDecision)
        chain = prompt | structured_llm

        result: RouteDecision = chain.invoke({"goal": goal})

        data = result.model_dump()

        department = str(data.get("department", "GENERAL")).upper().strip()
        data["department"] = (
            department if department in VALID_DEPARTMENTS else "GENERAL"
        )

        if data.get("action") == "none":
            data["app"] = None
            data["url"] = None

        return data

    except Exception as e:
        return {
            "department": "GENERAL",
            "message": f"Routing fallback: {str(e)}",
            "action": "none",
            "app": None,
            "url": None,
        }
