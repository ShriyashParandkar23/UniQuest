from django.urls import path
from .views import IngestionRunListView, search_universities, get_university, healthz

app_name = 'dataset'

urlpatterns = [
    path('universities/', search_universities, name='university-search'),
    path('universities/<str:university_id>/', get_university, name='university-detail'),
    path('ingestion/runs/', IngestionRunListView.as_view(), name='ingestion-runs'),
    path('healthz/', healthz, name='health-check'),
]
