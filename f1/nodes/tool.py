from ..tools import get_latest_or_next_race, get_race_by_name, get_f1_news, search_f1_web


def tool_node(state):
    tools = {
        "latest": get_latest_or_next_race,
        "specific": get_race_by_name,
        "news": get_f1_news,
        "general": search_f1_web,
    }
    result = tools[state["route"]].invoke({"question": state["question"]})
    return {"tool_result": result}
