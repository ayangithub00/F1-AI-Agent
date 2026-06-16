from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage, ToolMessage
from .tools import search_web, search_f1_news , get_f1_results
from langchain_mistralai import ChatMistralAI
from pathlib import Path
import os 
from dotenv import load_dotenv
load_dotenv()

env_path = Path(__file__).resolve().parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path, override=True)

vector_store = None

def get_vector_store():
    return vector_store

def load_knowledge_base(text: str):
    global vector_store
    from .rag import create_vector_store
    vector_store = create_vector_store(text)

def get_llm():
    return ChatMistralAI(
        model="mistral-small-latest",
        api_key=os.getenv("MISTRAL_API_KEY"),
        temperature=0
    )

def run_agent(question: str) -> str:
    llm = get_llm()
    tools = [search_web, search_f1_news, get_f1_results]
    llm_with_tools = llm.bind_tools(tools)
    tool_map = {t.name: t for t in tools}

    messages = [
        SystemMessage(content="You are an F1 expert assistant. Use the search tool to find accurate information before answering."),
        HumanMessage(content=question)
    ]

    for _ in range(5):
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
            

    return messages[-1].content