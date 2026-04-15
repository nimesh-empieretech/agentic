from app.tools.tools import developer_tool, qa_tool, devops_tool


def cto_agent(goal: str):
    goal_lower = goal.lower()

    if any(word in goal_lower for word in [
        "bug", "error", "fix", "develop", "code", "api", "website bug",
        "frontend", "backend", "react", "python", "fastapi", "node",
        "database", "login", "register"
    ]):
        result = developer_tool(goal)
        return {
            "department": "CTO",
            "assigned_agent": "Developer",
            "result": result,
            "status": "completed",
        }

    if any(word in goal_lower for word in [
        "qa", "test", "testing", "manual testing", "automation testing"
    ]):
        result = qa_tool(goal)
        return {
            "department": "CTO",
            "assigned_agent": "QA Engineer",
            "result": result,
            "status": "completed",
        }

    if any(word in goal_lower for word in [
        "server", "deployment", "devops", "nginx", "docker", "pm2",
        "infra", "infrastructure", "aws", "ubuntu", "hosting"
    ]):
        result = devops_tool(goal)
        return {
            "department": "CTO",
            "assigned_agent": "DevOps Engineer",
            "result": result,
            "status": "completed",
        }

    # fallback inside CTO
    result = developer_tool(goal)
    return {
        "department": "CTO",
        "assigned_agent": "Developer",
        "result": result,
        "status": "completed",
    }