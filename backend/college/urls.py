from django.urls import path
from .views import (
    CollegeListCreate,
    CollegeDetail,
    CollegeCSVUpload,
    CollegeExcelUpload,
)

urlpatterns = [
    path("", CollegeListCreate.as_view(), name="college-list-create"),
    path("<int:pk>/", CollegeDetail.as_view(), name="college-detail"),
    path("upload-csv/", CollegeCSVUpload.as_view(), name="college-upload-csv"),
    path("upload-excel/", CollegeExcelUpload.as_view(), name="college-upload-excel"),
]
