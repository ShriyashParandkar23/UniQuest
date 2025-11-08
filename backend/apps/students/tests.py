from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import StudentProfile

User = get_user_model()


class StudentProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            username='testuser',
            first_name='Test',
            last_name='User'
        )
    
    def test_create_student_profile(self):
        """Test creating a student profile."""
        profile = StudentProfile.objects.create(
            user=self.user,
            gpa=3.5,
            interests='Computer Science, AI',
            country_preference='US'
        )
        
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.gpa, 3.5)
        self.assertEqual(profile.country_preference, 'US')
    
    def test_test_score_methods(self):
        """Test test score getter and setter methods."""
        profile = StudentProfile.objects.create(user=self.user)
        
        profile.set_test_score('SAT', 1400)
        profile.set_test_score('toefl', 100)
        
        self.assertEqual(profile.get_test_score('SAT'), 1400)
        self.assertEqual(profile.get_test_score('TOEFL'), 100)


class StudentProfileAPITest(TestCase):
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
    
    def test_get_student_profile(self):
        """Test getting student profile creates one if doesn't exist."""
        response = self.client.get('/api/students/me/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data['data'])
        self.assertIsNone(response.data['error'])
    
    def test_update_student_profile(self):
        """Test updating student profile."""
        data = {
            'gpa': 3.7,
            'interests': 'Machine Learning',
            'country_preference': 'CA'
        }
        
        response = self.client.patch('/api/students/me/', data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['gpa'], '3.70')
        self.assertEqual(response.data['data']['country_preference'], 'CA')
