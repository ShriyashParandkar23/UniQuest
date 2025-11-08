from django.urls import path
from .views import RecommendationListView, run_recommendations

app_name = 'recommendations'

urlpatterns = [
    path('', RecommendationListView.as_view(), name='recommendation-list'),
    path('run/', run_recommendations, name='run-recommendations'),
]
