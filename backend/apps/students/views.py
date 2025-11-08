from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import StudentProfile
from .serializers import StudentProfileSerializer


class StudentProfileView(generics.RetrieveUpdateAPIView):
    """Get or update student profile."""
    serializer_class = StudentProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        """Get or create student profile for the current user."""
        profile, created = StudentProfile.objects.get_or_create(
            user=self.request.user
        )
        return profile
    
    def get(self, request, *args, **kwargs):
        """Get student profile."""
        profile = self.get_object()
        serializer = self.get_serializer(profile)
        return Response({
            'data': serializer.data,
            'error': None
        })
    
    def patch(self, request, *args, **kwargs):
        """Update student profile."""
        profile = self.get_object()
        serializer = self.get_serializer(profile, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'data': serializer.data,
                'error': None
            })
        else:
            return Response({
                'data': None,
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': 'Invalid data provided',
                    'details': serializer.errors
                }
            }, status=status.HTTP_400_BAD_REQUEST)
