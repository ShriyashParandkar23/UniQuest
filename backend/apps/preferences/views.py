from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Preference
from .serializers import PreferenceSerializer


class PreferenceView(generics.RetrieveUpdateAPIView):
    """Get or update user preferences."""
    serializer_class = PreferenceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        """Get or create preference for the current user."""
        preference, created = Preference.objects.get_or_create(
            user=self.request.user
        )
        return preference
    
    def get(self, request, *args, **kwargs):
        """Get user preferences."""
        preference = self.get_object()
        serializer = self.get_serializer(preference)
        return Response({
            'data': serializer.data,
            'error': None
        })
    
    def put(self, request, *args, **kwargs):
        """Update user preferences (full update)."""
        preference = self.get_object()
        serializer = self.get_serializer(preference, data=request.data)
        
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
                    'message': 'Invalid preferences data',
                    'details': serializer.errors
                }
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, *args, **kwargs):
        """Update user preferences (partial update)."""
        preference = self.get_object()
        serializer = self.get_serializer(preference, data=request.data, partial=True)
        
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
                    'message': 'Invalid preferences data',
                    'details': serializer.errors
                }
            }, status=status.HTTP_400_BAD_REQUEST)
