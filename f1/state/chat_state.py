from typing import TypedDict


class ChatState(TypedDict):
    question: str
    history: list
    tool_result: str
    answer: str
    verified: bool
