from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Preference

User = get_user_model()


class PreferenceModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            username='testuser',
            first_name='Test',
            last_name='User'
        )
    
    def test_create_preference_with_defaults(self):
        """Test creating preference gets default weights."""
        preference = Preference.objects.create(user=self.user)
        
        self.assertEqual(preference.user, self.user)
        self.assertIsInstance(preference.weights, dict)
        self.assertEqual(preference.get_weight('academics'), 0.3)
    
    def test_normalize_weights(self):
        """Test weight normalization."""
        preference = Preference.objects.create(
            user=self.user,
            weights={'academics': 0.6, 'interests': 0.6}
        )
        
        preference.normalize_weights()
        
        # Weights should sum to 1.0
        total = sum(preference.weights.values())
        self.assertAlmostEqual(total, 1.0, places=2)
    
    def test_set_weight_clamping(self):
        """Test weight clamping to [0, 1] range."""
        preference = Preference.objects.create(user=self.user)
        
        preference.set_weight('academics', 1.5)  # Above 1.0
        self.assertEqual(preference.get_weight('academics'), 1.0)
        
        preference.set_weight('interests', -0.5)  # Below 0.0
        self.assertEqual(preference.get_weight('interests'), 0.0)


class PreferenceAPITest(TestCase):
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
    
    def test_get_preferences(self):
        """Test getting preferences creates default if doesn't exist."""
        response = self.client.get('/api/students/preferences/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data['data']['weights'])
        self.assertIsNone(response.data['error'])
    
    def test_update_preferences(self):
        """Test updating preferences."""
        data = {
            'weights': {
                'academics': 0.5,
                'interests': 0.3,
                'career': 0.2
            }
        }
        
        response = self.client.put('/api/students/preferences/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that weights were normalized
        weights = response.data['data']['weights']
        total = sum(weights.values())
        self.assertAlmostEqual(total, 1.0, places=2)
    
    def test_invalid_weight_factor(self):
        """Test validation error for invalid weight factor."""
        data = {
            'weights': {
                'invalid_factor': 0.5
            }
        }
        
        response = self.client.put('/api/students/preferences/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNotNone(response.data['error'])
