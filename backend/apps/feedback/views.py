from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Feedback
from .serializers import FeedbackSerializer, FeedbackCreateSerializer
from ..recommendations.models import Recommendation


class FeedbackCreateView(generics.CreateAPIView):
    """Create feedback for a recommendation."""
    serializer_class = FeedbackCreateSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        """Create feedback for a specific recommendation."""
        recommendation_id = kwargs.get('recommendation_id')
        
        # Get the recommendation and verify it belongs to the user
        recommendation = get_object_or_404(
            Recommendation, 
            id=recommendation_id, 
            user=request.user
        )
        
        # Check if feedback already exists
        existing_feedback = Feedback.objects.filter(
            user=request.user,
            recommendation=recommendation
        ).first()
        
        if existing_feedback:
            return Response({
                'data': None,
                'error': {
                    'code': 'FEEDBACK_EXISTS',
                    'message': 'Feedback already exists for this recommendation',
                    'details': {'existing_feedback_id': existing_feedback.id}
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate and create feedback
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            feedback = serializer.save(
                user=request.user,
                recommendation=recommendation
            )
            
            # Return the created feedback
            response_serializer = FeedbackSerializer(feedback)
            return Response({
                'data': response_serializer.data,
                'error': None
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'data': None,
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': 'Invalid feedback data',
                    'details': serializer.errors
                }
            }, status=status.HTTP_400_BAD_REQUEST)


class FeedbackListView(generics.ListAPIView):
    """List user's feedback."""
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Get feedback for the current user."""
        return Feedback.objects.filter(user=self.request.user)
    
    def list(self, request, *args, **kwargs):
        """List feedback with standard error envelope."""
        try:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response({
                    'data': serializer.data,
                    'error': None
                })
            
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                'data': serializer.data,
                'error': None
            })
        except Exception as e:
            return Response({
                'data': None,
                'error': {
                    'code': 'INTERNAL_ERROR',
                    'message': 'Error retrieving feedback',
                    'details': str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
