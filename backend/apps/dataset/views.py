from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import IngestionRun
from .services import DatasetService
from .serializers import (
    IngestionRunSerializer, UniversitySearchSerializer, 
    UniversitySerializer, DatasetValidationSerializer
)


class UniversityPagination(PageNumberPagination):
    """Custom pagination for universities."""
    page_size = 20
    page_size_query_param = 'limit'
    max_page_size = 100


class IngestionRunListView(generics.ListAPIView):
    """List ingestion runs."""
    queryset = IngestionRun.objects.all()
    serializer_class = IngestionRunSerializer
    permission_classes = [IsAuthenticated]
    
    def list(self, request, *args, **kwargs):
        """List ingestion runs with standard error envelope."""
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
                    'message': 'Error retrieving ingestion runs',
                    'details': str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_universities(request):
    """Search universities with filters."""
    try:
        # Validate search parameters
        serializer = UniversitySearchSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response({
                'data': None,
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': 'Invalid search parameters',
                    'details': serializer.errors
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = serializer.validated_data
        
        # Extract search parameters
        filters = {}
        if validated_data.get('q'):
            filters['q'] = validated_data['q']
        if validated_data.get('country'):
            filters['country'] = validated_data['country']
        if validated_data.get('has_rank'):
            filters['has_rank'] = validated_data['has_rank']
        
        limit = validated_data.get('limit', 20)
        offset = validated_data.get('offset', 0)
        ordering = validated_data.get('ordering', 'display_name')
        
        # Search using dataset service
        dataset_service = DatasetService()
        universities = dataset_service.search_universities(
            filters=filters,
            limit=limit,
            offset=offset,
            ordering=ordering
        )
        
        # Serialize results
        university_serializer = UniversitySerializer(universities, many=True)
        
        return Response({
            'data': university_serializer.data,
            'error': None,
            'meta': {
                'count': len(universities),
                'limit': limit,
                'offset': offset,
                'filters': filters,
                'ordering': ordering
            }
        })
        
    except Exception as e:
        return Response({
            'data': None,
            'error': {
                'code': 'SEARCH_ERROR',
                'message': 'Error searching universities',
                'details': str(e)
            }
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_university(request, university_id):
    """Get a specific university by ID."""
    try:
        dataset_service = DatasetService()
        university = dataset_service.get_university(university_id)
        
        if not university:
            return Response({
                'data': None,
                'error': {
                    'code': 'NOT_FOUND',
                    'message': f'University not found: {university_id}',
                    'details': {}
                }
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Serialize result
        university_serializer = UniversitySerializer(university)
        
        return Response({
            'data': university_serializer.data,
            'error': None
        })
        
    except Exception as e:
        return Response({
            'data': None,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': f'Error retrieving university {university_id}',
                'details': str(e)
            }
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def healthz(request):
    """Health check endpoint."""
    try:
        # Check dataset service
        dataset_service = DatasetService()
        validation_result = dataset_service.validate_dataset()
        
        # Check database connection
        from django.db import connection
        db_ok = True
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
        except Exception:
            db_ok = False
        
        health_data = {
            'dataset_version': validation_result.get('version'),
            'duckdb_ok': validation_result.get('valid', False),
            'database_ok': db_ok,
            'dataset_stats': validation_result.get('stats', {})
        }
        
        # Determine overall health
        overall_ok = health_data['duckdb_ok'] and health_data['database_ok']
        
        return Response({
            'data': health_data,
            'error': None,
            'status': 'healthy' if overall_ok else 'unhealthy'
        }, status=status.HTTP_200_OK if overall_ok else status.HTTP_503_SERVICE_UNAVAILABLE)
        
    except Exception as e:
        return Response({
            'data': None,
            'error': {
                'code': 'HEALTH_CHECK_ERROR',
                'message': 'Error performing health check',
                'details': str(e)
            },
            'status': 'unhealthy'
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
