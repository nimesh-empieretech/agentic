from app.ai_router import smart_route_task

from app.agents.cto_agent import cto_agent
from app.agents.coo_agent import coo_agent
from app.agents.cfo_agent import cfo_agent
from app.agents.hr_agent import hr_agent
from app.agents.sales_agent import sales_agent
from app.agents.general_agent import general_agent


def ceo_agent(goal: str):
    route = smart_route_task(goal)
    department = route.get("department", "GENERAL")

    if route.get("action") == "open_app":
        return {
            "department": department,
            "assigned_agent": "APP_ACTION",
            "result": route.get("message", ""),
            "status": "completed",
            "action": route.get("action"),
            "app": route.get("app"),
            "url": route.get("url"),
        }

    if department == "CTO":
        result = cto_agent(goal)
    elif department == "COO":
        result = coo_agent(goal)
    elif department == "CFO":
        result = cfo_agent(goal)
    elif department == "HR":
        result = hr_agent(goal)
    elif department == "SALES":
        result = sales_agent(goal)
    else:
        result = general_agent(goal)

    return {
        "department": department,
        "assigned_agent": result.get("assigned_agent", department),
        "result": result.get("result", ""),
        "status": result.get("status", "completed"),
        "action": route.get("action", "none"),
        "app": route.get("app"),
        "url": route.get("url"),
    }
