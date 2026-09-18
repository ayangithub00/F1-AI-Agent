from langchain_groq import ChatGroq
try:
    from .config import GROQ_API_KEY
except ImportError:
    from config import GROQ_API_KEY


def get_llm():
    return ChatGroq(
        model="llama-3.1-8b-instant",
        api_key=GROQ_API_KEY,
        temperature=0,
    )
