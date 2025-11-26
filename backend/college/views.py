from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from .models import College
from .serializers import CollegeSerializer
import pandas as pd
import os
from rest_framework.permissions import AllowAny



class CollegeListCreate(APIView):
    def get(self, request):
        colleges = College.objects.all()
        serializer = CollegeSerializer(colleges, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CollegeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CollegeDetail(APIView):
    def get_object(self, pk):
        try:
            return College.objects.get(pk=pk)
        except College.DoesNotExist:
            return None

    def get(self, request, pk):
        college = self.get_object(pk)
        if not college:
            return Response({"error": "Not found"}, status=404)
        serializer = CollegeSerializer(college)
        return Response(serializer.data)

    def put(self, request, pk):
        college = self.get_object(pk)
        if not college:
            return Response({"error": "Not found"}, status=404)
        serializer = CollegeSerializer(college, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        college = self.get_object(pk)
        if not college:
            return Response({"error": "Not found"}, status=404)
        college.delete()
        return Response(status=204)

class CollegeCSVUpload(APIView):
    permission_classes = [AllowAny]  # <-- allows unauthenticated access

    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        uploaded_file = request.FILES.get("file")
        if not uploaded_file:
            return Response({"error": "No file uploaded"}, status=400)

        filename = uploaded_file.name
        ext = os.path.splitext(filename)[1].lower()

        if ext != ".csv":
            return Response({"error": "Only CSV files are supported"}, status=400)

        try:
            df = pd.read_csv(uploaded_file)
            expected_cols = [
                "world_rank","institution","country","national_rank",
                "quality_of_education","alumni_employment","quality_of_faculty",
                "publications","influence","citations","broad_impact",
                "patents","score","year"
            ]
            if not all(col in df.columns for col in expected_cols):
                return Response({"error": "CSV file missing required columns"}, status=400)

            created = 0
            for _, row in df.iterrows():
                College.objects.update_or_create(
                    world_rank=row["world_rank"],
                    institution=row["institution"],
                    year=row["year"],
                    defaults={
                        "country": row["country"],
                        "national_rank": row.get("national_rank"),
                        "quality_of_education": row.get("quality_of_education"),
                        "alumni_employment": row.get("alumni_employment"),
                        "quality_of_faculty": row.get("quality_of_faculty"),
                        "publications": row.get("publications"),
                        "influence": row.get("influence"),
                        "citations": row.get("citations"),
                        "broad_impact": row.get("broad_impact"),
                        "patents": row.get("patents"),
                        "score": row.get("score")
                    }
                )
                created += 1

            return Response({"message": f"{created} colleges added/updated successfully"}, status=201)

        except Exception as e:
            return Response({"error": str(e)}, status=500)

class CollegeExcelUpload(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        excel_file = request.FILES.get("file")
        if not excel_file:
            return Response({"error": "No file uploaded"}, status=400)

        try:
            df = pd.read_excel(excel_file)
            expected_cols = [
                "world_rank","institution","country","national_rank",
                "quality_of_education","alumni_employment","quality_of_faculty",
                "publications","influence","citations","broad_impact",
                "patents","score","year"
            ]
            if not all(col in df.columns for col in expected_cols):
                return Response({"error": "Excel file missing required columns"}, status=400)

            created = 0
            for _, row in df.iterrows():
                College.objects.update_or_create(
                    world_rank=row["world_rank"],
                    institution=row["institution"],
                    year=row["year"],
                    defaults={
                        "country": row["country"],
                        "national_rank": row.get("national_rank"),
                        "quality_of_education": row.get("quality_of_education"),
                        "alumni_employment": row.get("alumni_employment"),
                        "quality_of_faculty": row.get("quality_of_faculty"),
                        "publications": row.get("publications"),
                        "influence": row.get("influence"),
                        "citations": row.get("citations"),
                        "broad_impact": row.get("broad_impact"),
                        "patents": row.get("patents"),
                        "score": row.get("score")
                    }
                )
                created += 1

            return Response({"message": f"{created} colleges added/updated successfully"}, status=201)

        except Exception as e:
            return Response({"error": str(e)}, status=500)
