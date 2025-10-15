"""
Django management command to activate a dataset version.

This command updates the current dataset version pointer.

Example usage:
    python manage.py activate --version 2025.09
"""

import json
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.utils import timezone
from apps.dataset.models import IngestionRun


class Command(BaseCommand):
    help = 'Activate a dataset version as current'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--version',
            type=str,
            required=True,
            help='Version identifier to activate (e.g., 2025.09)'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force activation even if dataset validation fails'
        )
    
    def handle(self, *args, **options):
        version = options['version']
        force = options['force']
        
        base_path = Path(getattr(settings, 'DATASET_BASE_PATH', '/data'))
        curated_path = base_path / 'curated' / version
        
        self.stdout.write(f"Activating dataset version {version}")
        self.stdout.write(f"Dataset path: {curated_path}")
        
        # Validate the dataset exists and is complete
        if not force:
            validation_result = self._validate_dataset(curated_path)
            if not validation_result['valid']:
                raise CommandError(f"Dataset validation failed: {validation_result['error']}")
            
            self.stdout.write(self.style.SUCCESS("Dataset validation passed"))
        
        # Update the current version pointer
        current_file = base_path / 'current'
        
        try:
            with open(current_file, 'w') as f:
                f.write(version)
            
            self.stdout.write(self.style.SUCCESS(f"Successfully activated dataset version {version}"))
            
            # Create activation record
            run = IngestionRun.objects.create(
                source='activation',
                version=version,
                status='SUCCESS',
                finished_at=timezone.now(),
                stats={'activated_at': timezone.now().isoformat()}
            )
            
        except Exception as e:
            raise CommandError(f"Failed to activate dataset: {e}")
    
    def _validate_dataset(self, dataset_path):
        """Validate that the dataset is complete and usable."""
        
        # Check required files exist
        institutions_file = dataset_path / 'institutions.parquet'
        search_index_file = dataset_path / 'search_index.parquet'
        
        if not institutions_file.exists():
            return {
                'valid': False,
                'error': f'Institutions file not found: {institutions_file}'
            }
        
        if not search_index_file.exists():
            return {
                'valid': False,
                'error': f'Search index file not found: {search_index_file}'
            }
        
        try:
            # Test loading the files
            import polars as pl
            
            institutions_df = pl.read_parquet(institutions_file)
            search_df = pl.read_parquet(search_index_file)
            
            # Basic validation
            if len(institutions_df) == 0:
                return {
                    'valid': False,
                    'error': 'Institutions dataset is empty'
                }
            
            # Check required columns
            required_columns = ['id', 'display_name', 'country_code']
            missing_columns = [col for col in required_columns if col not in institutions_df.columns]
            
            if missing_columns:
                return {
                    'valid': False,
                    'error': f'Missing required columns: {missing_columns}'
                }
            
            self.stdout.write(f"Dataset contains {len(institutions_df)} institutions")
            
            # Count by country
            country_counts = institutions_df.group_by('country_code').agg(pl.count().alias('count'))
            top_countries = country_counts.sort('count', descending=True).head(5)
            
            self.stdout.write("Top countries by institution count:")
            for row in top_countries.iter_rows(named=True):
                self.stdout.write(f"  {row['country_code']}: {row['count']}")
            
            return {'valid': True}
            
        except Exception as e:
            return {
                'valid': False,
                'error': f'Error validating dataset: {e}'
            }
