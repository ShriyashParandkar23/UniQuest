from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Feedback
from ..recommendations.models import Recommendation

User = get_user_model()


class FeedbackModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            username='testuser',
            first_name='Test',
            last_name='User'
        )
        
        self.recommendation = Recommendation.objects.create(
            user=self.user,
            university_ref='openalex_id_123',
            score=0.85,
            rationale='Great match'
        )
    
    def test_create_feedback(self):
        """Test creating feedback."""
        feedback = Feedback.objects.create(
            user=self.user,
            recommendation=self.recommendation,
            rating=5,
            notes='Excellent recommendation!'
        )
        
        self.assertEqual(feedback.user, self.user)
        self.assertEqual(feedback.rating, 5)
        self.assertTrue(feedback.is_positive)
        self.assertFalse(feedback.is_negative)
    
    def test_feedback_properties(self):
        """Test feedback properties."""
        # Positive feedback
        positive_feedback = Feedback.objects.create(
            user=self.user,
            recommendation=self.recommendation,
            rating=4
        )
        self.assertTrue(positive_feedback.is_positive)
        self.assertFalse(positive_feedback.is_negative)
        
        # Negative feedback
        negative_feedback = Feedback.objects.create(
            user=self.user,
            recommendation=self.recommendation,
            rating=2
        )
        self.assertFalse(negative_feedback.is_positive)
        self.assertTrue(negative_feedback.is_negative)


class FeedbackAPITest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            username='testuser',
            first_name='Test',
            last_name='User'
        )
        
        self.recommendation = Recommendation.objects.create(
            user=self.user,
            university_ref='openalex_id_123',
            score=0.85,
            rationale='Great match'
        )
        
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
    
    def test_create_feedback(self):
        """Test creating feedback via API."""
        data = {
            'rating': 5,
            'notes': 'Excellent recommendation!'
        }
        
        response = self.client.post(
            f'/api/feedback/recommendations/{self.recommendation.id}/',
            data
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data['data'])
        self.assertIsNone(response.data['error'])
        
        # Verify feedback was created
        feedback = Feedback.objects.get(
            user=self.user,
            recommendation=self.recommendation
        )
        self.assertEqual(feedback.rating, 5)
    
    def test_duplicate_feedback_error(self):
        """Test error when creating duplicate feedback."""
        # Create initial feedback
        Feedback.objects.create(
            user=self.user,
            recommendation=self.recommendation,
            rating=4
        )
        
        # Try to create another feedback for the same recommendation
        data = {'rating': 5}
        response = self.client.post(
            f'/api/feedback/recommendations/{self.recommendation.id}/',
            data
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error']['code'], 'FEEDBACK_EXISTS')
    
    def test_list_feedback(self):
        """Test listing user feedback."""
        # Create some feedback
        Feedback.objects.create(
            user=self.user,
            recommendation=self.recommendation,
            rating=5
        )
        
        response = self.client.get('/api/feedback/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data['data'])
        self.assertIsNone(response.data['error'])
        self.assertEqual(len(response.data['data']), 1)
