from django.urls import path
from .views import FeedbackCreateView, FeedbackListView

app_name = 'feedback'

urlpatterns = [
    path('', FeedbackListView.as_view(), name='feedback-list'),
    path('recommendations/<int:recommendation_id>/', FeedbackCreateView.as_view(), name='feedback-create'),
]
