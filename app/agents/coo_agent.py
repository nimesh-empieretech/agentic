from app.tools import operations_tool


def coo_agent(goal: str):
    result = operations_tool(goal)
    return {
        "department": "COO",
        "assigned_agent": "Operations Manager",
        "result": result,
        "status": "completed",
    }