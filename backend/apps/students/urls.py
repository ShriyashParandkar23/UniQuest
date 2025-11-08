from django.urls import path
from .views import StudentProfileView

app_name = 'students'

urlpatterns = [
    path('me/', StudentProfileView.as_view(), name='student-profile'),
]
