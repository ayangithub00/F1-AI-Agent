from rest_framework.views import APIView
from rest_framework.response import Response
from .agent import run_agent, load_knowledge_base
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

class ChatView(APIView):
    def post(self, request):
        question = request.data.get("question")
        f1_data = request.data.get("f1_data", None)

        if f1_data:
            load_knowledge_base(f1_data)

        # get existing history from session
        history = request.session.get("chat_history", [])

        try:
            answer = run_agent(question, history)
            
            if isinstance(answer, list):
                answer = " ".join([item.get("text", "") for item in answer if isinstance(item, dict)])

            # save updated history to session
            history.append({"role": "user", "content": question})
            history.append({"role": "assistant", "content": answer})
            request.session["chat_history"] = history

            return Response({"answer": answer})
        except Exception as e:
            return Response({"error": str(e)}, status=500)