from ..llm import get_llm


def verify_node(state):
    prompt = f"""Check if this answer answers the question without inventing details.
If the information says the web search failed, allow only basic and timeless Formula 1 knowledge.
In that case, reject current teams, current season facts, race results, news, standings, and statistics.
Reply with only yes or no.

Question: {state['question']}

Information:
{state['tool_result']}

Answer:
{state['answer']}"""
    result = get_llm().invoke(prompt).content.strip().lower()
    return {"verified": result == "yes"}


def choose_verification(state):
    if state["verified"]:
        return "end"
    return "rewrite"
