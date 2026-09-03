from langgraph.graph import StateGraph, END
from .state.chat_state import ChatState
from .nodes.triage import triage_node, choose_route
from .nodes.tool import tool_node
from .nodes.answer import answer_node
from .nodes.verify import verify_node, choose_verification
from .nodes.rewrite import rewrite_node
from .nodes.unanswerable import unanswerable_node


workflow = StateGraph(ChatState)
workflow.add_node("triage", triage_node)
workflow.add_node("tool", tool_node)
workflow.add_node("answer", answer_node)
workflow.add_node("verify", verify_node)
workflow.add_node("rewrite", rewrite_node)
workflow.add_node("unanswerable", unanswerable_node)
workflow.set_entry_point("triage")
workflow.add_conditional_edges("triage", choose_route, {"tool": "tool", "unanswerable": "unanswerable"})
workflow.add_edge("tool", "answer")
workflow.add_edge("answer", "verify")
workflow.add_conditional_edges("verify", choose_verification, {"end": END, "rewrite": "rewrite"})
workflow.add_edge("rewrite", END)
workflow.add_edge("unanswerable", END)

chat_graph = workflow.compile()


def ask_question(question):
    result = chat_graph.invoke({
        "question": question,
        "route": "",
        "tool_result": "",
        "answer": "",
        "verified": False,
    })
    return result["answer"]
