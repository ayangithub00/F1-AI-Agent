try:
    from ..llm import get_llm
except ImportError:
    from llm import get_llm


def answer_node(state):
    history_list = state.get("history") or []
    history = "\n".join(
        f"{message.get('role', 'user')}: {message.get('content', '')}"
        for message in history_list
    )
    prompt = f"""Answer the Formula 1 question using the information below.
If the information says the web search failed, you may use only basic and timeless Formula 1 knowledge.
In that case, do not mention current teams, current season facts, race results, news, standings, or statistics.
Do not invent details.

Earlier conversation:
{history or "No earlier conversation."}

Question: {state['question']}

Information:
{state['tool_result']}"""
    import time
    import httpx

    llm = get_llm()
    for attempt in range(4):
        try:
            answer = llm.invoke(prompt).content
            return {"answer": answer}
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                time.sleep(2 * (attempt + 1))
                continue
            raise
        except Exception as e:
            err = str(e)
            if "429" in err or "rate_limited" in err.lower() or "rate limit" in err.lower():
                time.sleep(2 * (attempt + 1))
                continue
            raise

    return {"answer": "I'm a bit overloaded right now. Please try again in a few seconds!"}

