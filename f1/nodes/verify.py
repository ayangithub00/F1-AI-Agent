from ..llm import get_llm


def verify_node(state):
    prompt = f"""Check if this answer only uses the provided information and answers the question.
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
