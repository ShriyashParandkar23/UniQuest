"""
Integration tests for UniQuest API endpoints.

These tests verify the complete API workflow from authentication
through recommendations and feedback.
"""

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch
from tests.base import UniQuestAPITestCase, DatasetTestMixin
from tests.factories import UserFactory


class AuthenticationIntegrationTest(UniQuestAPITestCase):
    """Test authentication flow."""
    
    def test_complete_auth_flow(self):
        """Test complete authentication workflow."""
        # Create user
        user = UserFactory(email='test@example.com')
        
        # Login
        response = self.client.post('/api/auth/login/', {
            'email': 'test@example.com',
            'password': 'testpass123'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        
        # Use access token
        access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        response = self.client.get('/api/students/me/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Refresh token
        refresh_token = response.data['refresh']
        response = self.client.post('/api/auth/refresh/', {
            'refresh': refresh_token
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)


class StudentProfileIntegrationTest(UniQuestAPITestCase):
    """Test student profile management."""
    
    def test_profile_creation_and_update(self):
        """Test creating and updating student profile."""
        self.authenticate()
        
        # Get initial profile (should be created automatically)
        response = self.client.get('/api/students/me/')
        self.assertSuccessResponse(response)
        
        profile_data = response.data['data']
        self.assertEqual(profile_data['gpa'], str(self.student_profile.gpa))
        
        # Update profile
        update_data = {
            'gpa': 3.8,
            'interests': 'Updated interests',
            'test_scores': {'GRE': 330, 'TOEFL': 110}
        }
        
        response = self.client.patch('/api/students/me/', update_data)
        self.assertSuccessResponse(response)
        
        # Verify update
        response = self.client.get('/api/students/me/')
        profile_data = response.data['data']
        self.assertEqual(profile_data['gpa'], '3.80')
        self.assertEqual(profile_data['interests'], 'Updated interests')
        self.assertEqual(profile_data['test_scores'], {'GRE': 330, 'TOEFL': 110})


class PreferencesIntegrationTest(UniQuestAPITestCase):
    """Test preferences management."""
    
    def test_preferences_update_and_normalization(self):
        """Test updating preferences with normalization."""
        self.authenticate()
        
        # Update preferences with non-normalized weights
        update_data = {
            'weights': {
                'academics': 0.6,
                'interests': 0.6,  # This will cause normalization
                'career': 0.2
            }
        }
        
        response = self.client.put('/api/students/preferences/', update_data)
        self.assertSuccessResponse(response)
        
        # Check normalization occurred
        weights = response.data['data']['weights']
        total = sum(weights.values())
        self.assertAlmostEqual(total, 1.0, places=2)


class UniversitySearchIntegrationTest(UniQuestAPITestCase, DatasetTestMixin):
    """Test university search functionality."""
    
    @patch('apps.dataset.views.DatasetService')
    def test_university_search(self, mock_dataset_service):
        """Test university search with various filters."""
        self.authenticate()
        mock_service = self.mock_dataset_service(mock_dataset_service)
        
        # Search by query
        response = self.client.get('/api/universities/?q=stanford')
        self.assertSuccessResponse(response)
        
        # Search by country
        response = self.client.get('/api/universities/?country=US&has_rank=true')
        self.assertSuccessResponse(response)
        
        # Get specific university
        response = self.client.get('/api/universities/https://openalex.org/I97018004/')
        self.assertSuccessResponse(response)
        
        university = response.data['data']
        self.assertEqual(university['display_name'], 'Stanford University')


class RecommendationIntegrationTest(UniQuestAPITestCase, DatasetTestMixin):
    """Test recommendation generation and management."""
    
    @patch('apps.recommendations.views.DatasetService')
    def test_recommendation_workflow(self, mock_dataset_service):
        """Test complete recommendation workflow."""
        self.authenticate()
        mock_service = self.mock_dataset_service(mock_dataset_service)
        
        # Generate recommendations
        request_data = {
            'filters': {'country': 'US'},
            'weights': {'academics': 0.5, 'ranking': 0.3, 'research_activity': 0.2},
            'top_n': 5
        }
        
        response = self.client.post('/api/recommendations/run/', request_data)
        self.assertSuccessResponse(response)
        
        recommendations = response.data['data']
        self.assertGreater(len(recommendations), 0)
        
        # List recommendations
        response = self.client.get('/api/recommendations/')
        self.assertSuccessResponse(response)
        
        # Provide feedback on first recommendation
        if recommendations:
            rec_id = recommendations[0]['id']
            feedback_data = {
                'rating': 5,
                'notes': 'Excellent recommendation!'
            }
            
            response = self.client.post(
                f'/api/feedback/recommendations/{rec_id}/',
                feedback_data
            )
            self.assertSuccessResponse(response, status.HTTP_201_CREATED)
            
            # List feedback
            response = self.client.get('/api/feedback/')
            self.assertSuccessResponse(response)
            
            feedback_list = response.data['data']
            self.assertEqual(len(feedback_list), 1)
            self.assertEqual(feedback_list[0]['rating'], 5)


class SystemIntegrationTest(UniQuestAPITestCase):
    """Test system endpoints."""
    
    def test_health_check(self):
        """Test health check endpoint."""
        response = self.client.get('/api/healthz/')
        
        # Should return response (might be 200 or 503 depending on setup)
        self.assertIn(response.status_code, [
            status.HTTP_200_OK, 
            status.HTTP_503_SERVICE_UNAVAILABLE
        ])
        
        self.assertIn('status', response.data)
        self.assertIn('data', response.data)
    
    def test_ingestion_runs(self):
        """Test ingestion runs endpoint."""
        self.authenticate()
        
        response = self.client.get('/api/ingestion/runs/')
        self.assertSuccessResponse(response)


class ErrorHandlingIntegrationTest(UniQuestAPITestCase):
    """Test error handling across endpoints."""
    
    def test_unauthenticated_access(self):
        """Test that protected endpoints require authentication."""
        endpoints = [
            '/api/students/me/',
            '/api/students/preferences/',
            '/api/recommendations/',
            '/api/feedback/',
            '/api/universities/',
        ]
        
        for endpoint in endpoints:
            response = self.client.get(endpoint)
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
            self.assertErrorResponse(response, 'AUTHENTICATION_ERROR')
    
    def test_invalid_data_handling(self):
        """Test handling of invalid data."""
        self.authenticate()
        
        # Invalid GPA
        response = self.client.patch('/api/students/me/', {'gpa': 5.0})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertErrorResponse(response, 'VALIDATION_ERROR')
        
        # Invalid preference weights
        response = self.client.put('/api/students/preferences/', {
            'weights': {'invalid_factor': 0.5}
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertErrorResponse(response, 'VALIDATION_ERROR')
    
    def test_not_found_handling(self):
        """Test 404 error handling."""
        self.authenticate()
        
        response = self.client.get('/api/universities/nonexistent-id/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertErrorResponse(response, 'NOT_FOUND')
