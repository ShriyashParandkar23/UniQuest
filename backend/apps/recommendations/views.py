from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from .models import Recommendation
from .serializers import RecommendationSerializer, RecommendationRequestSerializer
from ..dataset.services import DatasetService
from .services import RecommendationService


class RecommendationPagination(PageNumberPagination):
    """Custom pagination for recommendations."""
    page_size = 20
    page_size_query_param = 'limit'
    max_page_size = 100


class RecommendationListView(generics.ListAPIView):
    """List user's recommendations."""
    serializer_class = RecommendationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = RecommendationPagination
    
    def get_queryset(self):
        """Get recommendations for the current user."""
        return Recommendation.objects.filter(user=self.request.user)
    
    def list(self, request, *args, **kwargs):
        """List recommendations with standard error envelope."""
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
                    'message': 'Error retrieving recommendations',
                    'details': str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def run_recommendations(request):
    """Generate new recommendations for the user."""
    try:
        # Validate request data
        serializer = RecommendationRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'data': None,
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': 'Invalid request data',
                    'details': serializer.errors
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = serializer.validated_data
        filters = validated_data.get('filters', {})
        weights = validated_data.get('weights', {})
        top_n = validated_data.get('top_n', 20)
        
        # Initialize recommendation service
        recommendation_service = RecommendationService()
        
        # TODO (Vishal): Before generating recommendations, you might want to call your LLM API
        # to pre-process or enhance the user filters and weights based on their profile
        # Example:
        # enhanced_filters = requests.post('https://your-llm-api.com/enhance-filters', json={
        #     'user_profile': user_profile,
        #     'original_filters': filters,
        #     'original_weights': weights
        # }).json()
        
        # Generate recommendations (with LLM integration inside the service)
        recommendations = recommendation_service.generate_recommendations(
            user=request.user,
            filters=filters,
            weights=weights,
            top_n=top_n
        )
        
        # Serialize and return
        recommendation_serializer = RecommendationSerializer(recommendations, many=True)
        
        return Response({
            'data': recommendation_serializer.data,
            'error': None,
            'meta': {
                'count': len(recommendations),
                'filters_applied': filters,
                'weights_used': weights
            }
        })
        
    except Exception as e:
        return Response({
            'data': None,
            'error': {
                'code': 'RECOMMENDATION_ERROR',
                'message': 'Error generating recommendations',
                'details': str(e)
            }
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
