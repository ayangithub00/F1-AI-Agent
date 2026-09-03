from ..llm import get_llm


def triage_node(state):
    prompt = f"""Classify this user question about Formula 1.

Question: {state['question']}

Reply with only one word:
latest for latest race or next race,
specific for one named race,
news for current news,
general for another Formula 1 question,
unanswerable if it is not about Formula 1 or cannot be answered safely."""
    route = get_llm().invoke(prompt).content.strip().lower()
    allowed_routes = ["latest", "specific", "news", "general", "unanswerable"]
    if route not in allowed_routes:
        route = "unanswerable"
    return {"route": route}


def choose_route(state):
    if state["route"] == "unanswerable":
        return "unanswerable"
    return "tool"
