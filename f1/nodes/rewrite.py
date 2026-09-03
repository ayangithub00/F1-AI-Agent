from ..llm import get_llm


def rewrite_node(state):
    prompt = f"""Rewrite this answer using only the provided information.
If the information does not support an answer, say that you do not have enough reliable information.

Question: {state['question']}

Information:
{state['tool_result']}

Answer to rewrite:
{state['answer']}"""
    answer = get_llm().invoke(prompt).content
    return {"answer": answer}
