from app.tools.ai_helper import generate_ai_response


def developer_tool(goal: str) -> str:
    return generate_ai_response("Software Developer", goal)


def qa_tool(goal: str) -> str:
    return generate_ai_response("QA Engineer", goal)


def devops_tool(goal: str) -> str:
    return generate_ai_response("DevOps Engineer", goal)


def operations_tool(goal: str) -> str:
    return generate_ai_response("Operations Manager", goal)


def finance_tool(goal: str) -> str:
    return generate_ai_response("Finance Expert", goal)


def hr_tool(goal: str) -> str:
    return generate_ai_response("HR Manager", goal)


def sales_tool(goal: str) -> str:
    return generate_ai_response("Sales Consultant", goal)


def general_tool(goal: str) -> str:
    return generate_ai_response("Customer Support Assistant", goal)