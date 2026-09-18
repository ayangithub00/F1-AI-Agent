from langchain_groq import ChatGroq
try:
    from .config import GROQ_API_KEY
except ImportError:
    from config import GROQ_API_KEY


def get_llm():
    return ChatGroq(
        model="llama3-8b-8192",
        api_key=GROQ_API_KEY,
        temperature=0,
    )
