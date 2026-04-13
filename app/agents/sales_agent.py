from app.tools import sales_tool


def sales_agent(goal: str):
    result = sales_tool(goal)
    return {
        "department": "Sales",
        "assigned_agent": "Clients",
        "result": result,
        "status": "completed",
    }
