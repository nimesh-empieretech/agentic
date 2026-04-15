from app.ai_router import smart_route_task
from app.agents.cto_agent import cto_agent
from app.agents.coo_agent import coo_agent
from app.agents.cfo_agent import cfo_agent
from app.agents.hr_agent import hr_agent
from app.agents.sales_agent import sales_agent
from app.agents.general_agent import general_agent


def ceo_agent(goal: str):
    department = smart_route_task(goal)

    if department == "CTO":
        return cto_agent(goal)

    if department == "COO":
        return coo_agent(goal)

    if department == "CFO":
        return cfo_agent(goal)

    if department == "HR":
        return hr_agent(goal)

    if department == "SALES":
        return sales_agent(goal)

    if department == "GENERAL":
        return general_agent(goal)

    return {
        "department": "CEO",
        "assigned_agent": "CEO",
        "result": f"Could not route task: {goal}",
        "status": "failed",
    }