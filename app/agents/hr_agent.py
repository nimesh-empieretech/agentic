from app.tools import hr_tool


def hr_agent(goal: str):
    result = hr_tool(goal)
    return {
        "department": "HR",
        "assigned_agent": "Employees",
        "result": result,
        "status": "completed",
    }
