from django.urls import path, include
from .views import health_check, get_student_info

urlpatterns = [
    path('', get_student_info, name='health_check'),
]



