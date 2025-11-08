from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch, MagicMock
from .models import Recommendation
from .services import RecommendationService

User = get_user_model()


class RecommendationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            username='testuser',
            first_name='Test',
            last_name='User'
        )
    
    def test_create_recommendation(self):
        """Test creating a recommendation."""
        recommendation = Recommendation.objects.create(
            user=self.user,
            university_ref='openalex_id_123',
            program='Computer Science',
            score=0.85,
            rationale='Great match for your profile'
        )
        
        self.assertEqual(recommendation.user, self.user)
        self.assertEqual(recommendation.score, 0.85)
        self.assertEqual(recommendation.score_percentage, 85)
    
    def test_recommendation_ordering(self):
        """Test recommendations are ordered by date and score."""
        rec1 = Recommendation.objects.create(
            user=self.user,
            university_ref='openalex_id_1',
            score=0.7,
            rationale='Good match'
        )
        rec2 = Recommendation.objects.create(
            user=self.user,
            university_ref='openalex_id_2',
            score=0.9,
            rationale='Excellent match'
        )
        
        recommendations = list(Recommendation.objects.all())
        # Should be ordered by generated_at desc, then score desc
        self.assertEqual(recommendations[0], rec2)


class RecommendationServiceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            username='testuser',
            first_name='Test',
            last_name='User'
        )
        self.service = RecommendationService()
    
    @patch('apps.recommendations.services.DatasetService')
    def test_generate_recommendations(self, mock_dataset_service):
        """Test generating recommendations."""
        # Mock dataset service response
        mock_dataset_service.return_value.recommend.return_value = [
            {
                'id': 'openalex_id_1',
                'display_name': 'Stanford University',
                'score': 0.9,
                'country_code': 'US',
                'webometrics_rank': 5
            },
            {
                'id': 'openalex_id_2',
                'display_name': 'MIT',
                'score': 0.85,
                'country_code': 'US',
                'works_count': 50000
            }
        ]
        
        filters = {'country': 'US'}
        weights = {'academics': 0.5, 'ranking': 0.3, 'research_activity': 0.2}
        
        recommendations = self.service.generate_recommendations(
            user=self.user,
            filters=filters,
            weights=weights,
            top_n=2
        )
        
        self.assertEqual(len(recommendations), 2)
        self.assertEqual(recommendations[0].university_ref, 'openalex_id_1')
        self.assertEqual(recommendations[0].score, 0.9)
        self.assertIn('Stanford University', recommendations[0].rationale)


class RecommendationAPITest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            username='testuser',
            first_name='Test',
            last_name='User'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
    
    def test_list_recommendations(self):
        """Test listing user recommendations."""
        # Create some recommendations
        Recommendation.objects.create(
            user=self.user,
            university_ref='openalex_id_1',
            score=0.9,
            rationale='Great match'
        )
        
        response = self.client.get('/api/recommendations/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data['data'])
        self.assertIsNone(response.data['error'])
    
    @patch('apps.recommendations.views.RecommendationService')
    def test_run_recommendations(self, mock_service):
        """Test running recommendations endpoint."""
        # Mock service
        mock_recommendation = MagicMock()
        mock_recommendation.id = 1
        mock_recommendation.university_ref = 'openalex_id_1'
        mock_recommendation.score = 0.9
        mock_recommendation.rationale = 'Great match'
        mock_recommendation.filters = {}
        mock_recommendation.weights = {}
        mock_recommendation.generated_at = '2023-01-01T00:00:00Z'
        mock_recommendation.program = None
        mock_recommendation.score_percentage = 90
        
        mock_service.return_value.generate_recommendations.return_value = [
            mock_recommendation
        ]
        
        data = {
            'filters': {'country': 'US'},
            'weights': {'academics': 0.5},
            'top_n': 10
        }
        
        response = self.client.post('/api/recommendations/run/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data['data'])
        self.assertIsNone(response.data['error'])
