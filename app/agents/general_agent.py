from app.tools.tools import general_tool


def general_agent(goal: str):
    result = general_tool(goal)
    return {
        "department": "GENERAL",
        "assigned_agent": "Support Assistant",
        "result": result,
        "status": "completed",
    }
