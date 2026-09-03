try:
    from ..tools import get_latest_or_next_race, get_race_by_name, get_f1_news, search_f1_web
except ImportError:
    from tools import get_latest_or_next_race, get_race_by_name, get_f1_news, search_f1_web


def tool_node(state):
    question = state["question"].lower().strip()
    greetings = ["hi", "hello", "hey", "who are you", "what can you do", "help"]
    if question in greetings or any(question.startswith(g + " ") for g in greetings):
        return {
            "tool_result": "Conversational greeting. Greet the user warmly and introduce yourself as an AI assistant specialized in Formula 1 racing, race results, calendar, and news."
        }

    race_words = ["latest", "last", "previous", "recent", "next", "race results"]
    race_names = ["australia", "japan", "bahrain", "saudi", "miami", "monaco", "spain", "canada", "austria", "britain", "silverstone", "belgium", "hungary", "netherlands", "italy", "monza", "azerbaijan", "singapore", "united states", "mexico", "brazil", "las vegas", "qatar", "abu dhabi"]

    if "news" in question:
        result = get_f1_news.invoke({"question": state["question"]})
    elif any(word in question for word in race_words):
        result = get_latest_or_next_race.invoke({"question": state["question"]})
    elif any(name in question for name in race_names):
        result = get_race_by_name.invoke({"question": state["question"]})
    else:
        result = search_f1_web.invoke({"question": state["question"]})

    return {"tool_result": result}
