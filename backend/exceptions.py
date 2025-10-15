"""
Custom exception handler for UniQuest API.

Provides consistent error response format across all endpoints.
"""

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom exception handler that returns errors in a consistent format.
    
    Expected format:
    {
        "data": null,
        "error": {
            "code": "ERROR_CODE",
            "message": "Human readable message",
            "details": {...} // Optional additional details
        }
    }
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)
    
    if response is not None:
        # Log the exception
        logger.error(f"API Exception: {exc}", exc_info=True, extra={
            'request': context.get('request'),
            'view': context.get('view'),
        })
        
        # Map common DRF error codes to our format
        error_code_mapping = {
            400: 'VALIDATION_ERROR',
            401: 'AUTHENTICATION_ERROR',
            403: 'PERMISSION_ERROR',
            404: 'NOT_FOUND',
            405: 'METHOD_NOT_ALLOWED',
            429: 'RATE_LIMIT_EXCEEDED',
            500: 'INTERNAL_ERROR',
        }
        
        error_code = error_code_mapping.get(response.status_code, 'API_ERROR')
        error_message = 'An error occurred'
        error_details = {}
        
        # Extract error information based on exception type
        if hasattr(exc, 'detail'):
            if isinstance(exc.detail, dict):
                error_details = exc.detail
                if 'detail' in error_details:
                    error_message = str(error_details.pop('detail'))
                elif 'non_field_errors' in error_details:
                    error_message = str(error_details['non_field_errors'][0])
                else:
                    error_message = 'Validation failed'
            elif isinstance(exc.detail, list):
                error_message = str(exc.detail[0])
            else:
                error_message = str(exc.detail)
        
        # Override for specific exceptions
        if response.status_code == status.HTTP_401_UNAUTHORIZED:
            error_message = 'Authentication credentials were not provided or are invalid'
        elif response.status_code == status.HTTP_403_FORBIDDEN:
            error_message = 'You do not have permission to perform this action'
        elif response.status_code == status.HTTP_404_NOT_FOUND:
            error_message = 'The requested resource was not found'
        elif response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED:
            error_message = 'Method not allowed'
        elif response.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
            error_message = 'Too many requests. Please try again later'
        
        # Build the custom response
        custom_response_data = {
            'data': None,
            'error': {
                'code': error_code,
                'message': error_message,
                'details': error_details
            }
        }
        
        response.data = custom_response_data
    
    return response
