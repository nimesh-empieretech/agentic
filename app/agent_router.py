from app.agents.ceo_agent import ceo_agent


def route_task(goal: str):
    return ceo_agent(goal)
