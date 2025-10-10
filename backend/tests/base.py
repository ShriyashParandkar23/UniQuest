"""
Base test classes and utilities for UniQuest tests.
"""

from django.test import TestCase, TransactionTestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .factories import UserFactory, StudentProfileFactory, PreferenceFactory

User = get_user_model()


class UniQuestTestCase(TestCase):
    """Base test case with common utilities."""
    
    @classmethod
    def setUpTestData(cls):
        """Set up test data for the TestCase."""
        cls.user = UserFactory()
        cls.student_profile = StudentProfileFactory(user=cls.user)
        cls.preferences = PreferenceFactory(user=cls.user)
    
    def setUp(self):
        """Set up for each test method."""
        pass


class UniQuestAPITestCase(APITestCase):
    """Base API test case with authentication utilities."""
    
    @classmethod
    def setUpTestData(cls):
        """Set up test data for the API TestCase."""
        cls.user = UserFactory()
        cls.student_profile = StudentProfileFactory(user=cls.user)
        cls.preferences = PreferenceFactory(user=cls.user)
    
    def setUp(self):
        """Set up for each test method."""
        self.client = APIClient()
    
    def authenticate(self, user=None):
        """Authenticate a user for API calls."""
        user = user or self.user
        self.client.force_authenticate(user=user)
    
    def get_tokens(self, user=None):
        """Get JWT tokens for a user."""
        user = user or self.user
        from rest_framework_simplejwt.tokens import RefreshToken
        
        refresh = RefreshToken.for_user(user)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }
    
    def assertErrorResponse(self, response, expected_code=None):
        """Assert that response is an error with expected format."""
        self.assertIsNone(response.data.get('data'))
        self.assertIsNotNone(response.data.get('error'))
        
        error = response.data['error']
        self.assertIn('code', error)
        self.assertIn('message', error)
        
        if expected_code:
            self.assertEqual(error['code'], expected_code)
    
    def assertSuccessResponse(self, response, expected_status=status.HTTP_200_OK):
        """Assert that response is successful with expected format."""
        self.assertEqual(response.status_code, expected_status)
        self.assertIsNotNone(response.data.get('data'))
        self.assertIsNone(response.data.get('error'))


class DatasetTestMixin:
    """Mixin for tests that need mock dataset functionality."""
    
    def setUp(self):
        """Set up mock dataset."""
        super().setUp()
        self.mock_universities = [
            {
                'id': 'https://openalex.org/I97018004',
                'display_name': 'Stanford University',
                'canonical_name': 'stanford-university',
                'country_code': 'US',
                'homepage_url': 'https://stanford.edu',
                'webometrics_rank': 5,
                'works_count': 50000,
                'cited_by_count': 100000,
                'geo_latitude': 37.4275,
                'geo_longitude': -122.1697,
                'has_rank': True
            },
            {
                'id': 'https://openalex.org/I136199984',
                'display_name': 'Massachusetts Institute of Technology',
                'canonical_name': 'mit',
                'country_code': 'US',
                'homepage_url': 'https://mit.edu',
                'webometrics_rank': 3,
                'works_count': 60000,
                'cited_by_count': 120000,
                'geo_latitude': 42.3601,
                'geo_longitude': -71.0942,
                'has_rank': True
            }
        ]
    
    def mock_dataset_service(self, mock_class):
        """Configure mock dataset service."""
        mock_service = mock_class.return_value
        mock_service.search_universities.return_value = self.mock_universities
        mock_service.get_university.return_value = self.mock_universities[0]
        mock_service.recommend.return_value = [
            {**uni, 'score': 0.9 - i * 0.1} 
            for i, uni in enumerate(self.mock_universities)
        ]
        mock_service.validate_dataset.return_value = {
            'valid': True,
            'version': '2025.09',
            'stats': {'total_institutions': 10000}
        }
        return mock_service
