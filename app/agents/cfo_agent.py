from app.tools import finance_tool


def cfo_agent(goal: str):
    result = finance_tool(goal)
    return {
        "department": "CFO",
        "assigned_agent": "Finance Expert",
        "result": result,
        "status": "completed",
    }