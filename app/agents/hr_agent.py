from app.tools import hr_tool


def hr_agent(goal: str):
    result = hr_tool(goal)
    return {
        "department": "HR",
        "assigned_agent": "HR Manager",
        "result": result,
        "status": "completed",
    }