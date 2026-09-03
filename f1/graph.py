from langgraph.graph import StateGraph, END
try:
    from .state.chat_state import ChatState
    from .nodes.tool import tool_node
    from .nodes.answer import answer_node
except ImportError:
    from state.chat_state import ChatState
    from nodes.tool import tool_node
    from nodes.answer import answer_node


workflow = StateGraph(ChatState)
workflow.add_node("tool", tool_node)
workflow.add_node("answer", answer_node)
workflow.set_entry_point("tool")
workflow.add_edge("tool", "answer")
workflow.add_edge("answer", END)

chat_graph = workflow.compile()


def ask_question(question, history):
    result = chat_graph.invoke({
        "question": question,
        "history": history,
        "tool_result": "",
        "answer": "",
        "verified": False,
    })
    return result["answer"]
