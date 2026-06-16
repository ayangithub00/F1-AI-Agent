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

        try:
            answer = run_agent(question)
            if isinstance(answer, list):
                answer = " ".join([item.get("text", "") for item in answer if isinstance(item, dict)])

            return Response({"answer": answer})
        except Exception as e:
            return Response({"error": str(e)}, status=500)