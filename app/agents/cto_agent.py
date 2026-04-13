from app.tools import developer_tool, qa_tool, devops_tool


def cto_agent(goal: str):
    goal_lower = goal.lower()

    if any(
        word in goal_lower
        for word in ["bug", "error", "fix", "develop", "code", "api", "website"]
    ):
        result = developer_tool(goal)
        return {
            "department": "CTO",
            "assigned_agent": "Developers",
            "result": result,
            "status": "completed",
        }

    if any(word in goal_lower for word in ["qa", "test", "testing"]):
        result = qa_tool(goal)
        return {
            "department": "CTO",
            "assigned_agent": "QA",
            "result": result,
            "status": "completed",
        }

    result = devops_tool(goal)
    return {
        "department": "CTO",
        "assigned_agent": "DevOps",
        "result": result,
        "status": "completed",
    }
