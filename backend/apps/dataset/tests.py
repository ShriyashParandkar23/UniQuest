from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch, MagicMock
from .models import IngestionRun
from .services import DatasetService

User = get_user_model()


class IngestionRunModelTest(TestCase):
    def test_create_ingestion_run(self):
        """Test creating an ingestion run."""
        run = IngestionRun.objects.create(
            source='openalex',
            version='2025.09',
            status='SUCCESS',
            stats={'institutions': 10000}
        )
        
        self.assertEqual(run.source, 'openalex')
        self.assertEqual(run.version, '2025.09')
        self.assertTrue(run.is_completed)
        self.assertEqual(run.get_stat('institutions'), 10000)
    
    def test_ingestion_run_properties(self):
        """Test ingestion run properties."""
        run = IngestionRun.objects.create(
            source='webometrics',
            version='2025.09',
            status='RUNNING'
        )
        
        self.assertFalse(run.is_completed)
        run.status = 'SUCCESS'
        self.assertTrue(run.is_completed)


class DatasetServiceTest(TestCase):
    def setUp(self):
        self.service = DatasetService()
    
    @patch('apps.dataset.services.Path.exists')
    @patch('apps.dataset.services.duckdb.connect')
    def test_search_universities(self, mock_connect, mock_exists):
        """Test university search functionality."""
        # Mock file existence
        mock_exists.return_value = True
        
        # Mock DuckDB connection and results
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.execute.return_value.fetchall.return_value = [
            ('openalex_1', 'Stanford University', 'stanford-university', 'US', 
             'https://stanford.edu', 5, 50000, 100000, 37.4275, -122.1697)
        ]
        mock_conn.description = [
            ('id',), ('display_name',), ('canonical_name',), ('country_code',),
            ('homepage_url',), ('webometrics_rank',), ('works_count',), 
            ('cited_by_count',), ('geo_latitude',), ('geo_longitude',)
        ]
        
        # Test search
        results = self.service.search_universities(
            filters={'country': 'US'},
            limit=10
        )
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['display_name'], 'Stanford University')
        self.assertTrue(results[0]['has_rank'])
    
    def test_validate_dataset_file_not_found(self):
        """Test dataset validation when file doesn't exist."""
        # This will fail because we don't have actual dataset files
        result = self.service.validate_dataset()
        
        self.assertFalse(result['valid'])
        self.assertIn('not found', result['error'])


class DatasetAPITest(TestCase):
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
    
    def test_list_ingestion_runs(self):
        """Test listing ingestion runs."""
        IngestionRun.objects.create(
            source='openalex',
            version='2025.09',
            status='SUCCESS'
        )
        
        response = self.client.get('/api/ingestion/runs/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data['data'])
        self.assertIsNone(response.data['error'])
    
    @patch('apps.dataset.views.DatasetService')
    def test_search_universities(self, mock_service):
        """Test university search endpoint."""
        # Mock service response
        mock_service.return_value.search_universities.return_value = [
            {
                'id': 'openalex_1',
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
            }
        ]
        
        response = self.client.get('/api/universities/?q=stanford&country=US')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data['data'])
        self.assertIsNone(response.data['error'])
        self.assertIn('meta', response.data)
    
    def test_health_check(self):
        """Test health check endpoint."""
        # This will likely fail due to missing dataset files, but tests the endpoint
        response = self.client.get('/api/healthz/')
        
        # Should return a response (either 200 or 503)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_503_SERVICE_UNAVAILABLE])
        self.assertIn('status', response.data)
