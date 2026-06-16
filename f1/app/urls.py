from django.urls import path
from .views import ChatView , index

urlpatterns = [
    path('', index),
    path('api/chat/', ChatView.as_view()),
]