from django.urls import path
from .views import PreferenceView

app_name = 'preferences'

urlpatterns = [
    path('', PreferenceView.as_view(), name='preferences'),
]
