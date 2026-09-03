from langchain_mistralai import ChatMistralAI
try:
    from .config import MISTRAL_API_KEY
except ImportError:
    from config import MISTRAL_API_KEY


def get_llm():
    return ChatMistralAI(
        model="mistral-small-latest",
        api_key=MISTRAL_API_KEY,
        temperature=0,
    )
