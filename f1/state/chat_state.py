from typing import TypedDict


class ChatState(TypedDict):
    question: str
    route: str
    tool_result: str
    answer: str
    verified: bool
