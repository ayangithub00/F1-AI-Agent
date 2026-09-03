from ..llm import get_llm


def answer_node(state):
    prompt = f"""Answer the Formula 1 question using only the information below.
Do not add facts that are not in the information. If the information is missing, say that clearly.

Question: {state['question']}

Information:
{state['tool_result']}"""
    answer = get_llm().invoke(prompt).content
    return {"answer": answer}
