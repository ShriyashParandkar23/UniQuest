from django.urls import path
from .views import GeminiChatAPIView

urlpatterns = [
    path("chat/", GeminiChatAPIView.as_view(), name="gemini-chat"),
]
