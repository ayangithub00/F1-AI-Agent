from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage, ToolMessage
from .tools import search_web, search_f1_news, get_f1_results, get_race_by_name
from langchain_mistralai import ChatMistralAI
from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv("/Users/ayanislam/Documents/LLM Project/F1 Project/f1/.env")
# env_path = Path(__file__).resolve().parent.parent.parent / '.env'
# load_dotenv(dotenv_path=env_path, override=True)

vector_store = None

def get_vector_store():
    return vector_store

def load_knowledge_base(text: str):
    global vector_store
    from .rag import create_vector_store
    vector_store = create_vector_store(text)

# def get_llm():
#     return ChatMistralAI(
#         model="mistral-small-latest",
#         api_key=os.getenv("MISTRAL_API_KEY"),
#         temperature=0
#     )

def get_llm():
    key = os.getenv("MISTRAL_API_KEY")
    print("KEY BEING USED:", key)  # ← add this
    return ChatMistralAI(
        model="mistral-small-latest",
        api_key=key,
        temperature=0
    )

def run_agent(question: str, history: list = []) -> str:
    llm = get_llm()
    tools = [search_web, search_f1_news, get_f1_results, get_race_by_name]
    llm_with_tools = llm.bind_tools(tools)
    tool_map = {t.name: t for t in tools}

    # build messages with history
    messages = [
        SystemMessage(content="""You are an F1 expert assistant for the 2026 Formula 1 season.
Today's date is June 17, 2026.

TOOL USAGE RULES:
- For "latest race" or "next race" questions, use get_f1_results.
- For questions about a SPECIFIC race by name (Monaco, Barcelona, Silverstone, etc.), ALWAYS use get_race_by_name tool, NOT search_web.
- Only use search_web for general F1 concepts, not for race results.
- Default to 2026 season data unless the user explicitly asks about 2024 or 2025.
- If the user specifically asks about 2024 or 2025, you may use search_web for that historical data."""),
    ]

    # add previous conversation history
    for msg in history:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            messages.append(SystemMessage(content=msg["content"]))

    # add current question
    messages.append(HumanMessage(content=question))

    for _ in range(3):
        response = llm_with_tools.invoke(messages)
        messages.append(response)

        if not response.tool_calls:
            break

        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            if tool_name in tool_map:
                result = tool_map[tool_name].invoke(tool_args)
                messages.append(ToolMessage(
                    content=str(result),
                    tool_call_id=tool_call["id"]
                ))

    messages.append(SystemMessage(content="Now provide a complete and accurate answer based on the search results. Do not call any more tools."))
    final = llm.invoke(messages)
    return final.content