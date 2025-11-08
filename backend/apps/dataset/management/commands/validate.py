"""
Django management command to validate a dataset version.

This command performs comprehensive validation of dataset files.

Example usage:
    python manage.py validate --version 2025.09
"""

import json
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from apps.dataset.services import DatasetService


class Command(BaseCommand):
    help = 'Validate a dataset version'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--version',
            type=str,
            help='Version identifier to validate (defaults to current active version)'
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Show detailed validation information'
        )
    
    def handle(self, *args, **options):
        version = options['version']
        verbose = options['verbose']
        
        base_path = Path(getattr(settings, 'DATASET_BASE_PATH', '/data'))
        
        if version:
            dataset_path = base_path / 'curated' / version
            self.stdout.write(f"Validating dataset version {version}")
        else:
            # Use current active version
            dataset_service = DatasetService()
            version = dataset_service.current_version
            dataset_path = dataset_service.get_dataset_path('').parent
            self.stdout.write(f"Validating current active dataset version {version}")
        
        self.stdout.write(f"Dataset path: {dataset_path}")
        
        # Perform validation
        validation_result = self._validate_dataset(dataset_path, verbose)
        
        if validation_result['valid']:
            self.stdout.write(self.style.SUCCESS("✓ Dataset validation passed"))
            
            if verbose:
                self._print_detailed_stats(validation_result['stats'])
        else:
            self.stdout.write(self.style.ERROR(f"✗ Dataset validation failed: {validation_result['error']}"))
            raise CommandError("Dataset validation failed")
    
    def _validate_dataset(self, dataset_path, verbose=False):
        """Perform comprehensive dataset validation."""
        
        validation_results = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'stats': {}
        }
        
        # Check file existence
        institutions_file = dataset_path / 'institutions.parquet'
        search_index_file = dataset_path / 'search_index.parquet'
        
        if not institutions_file.exists():
            validation_results['errors'].append(f'Institutions file not found: {institutions_file}')
            validation_results['valid'] = False
        
        if not search_index_file.exists():
            validation_results['warnings'].append(f'Search index file not found: {search_index_file}')
        
        if not validation_results['valid']:
            return validation_results
        
        try:
            # Load and validate data structure
            import polars as pl
            
            self.stdout.write("Loading dataset files...")
            institutions_df = pl.read_parquet(institutions_file)
            
            # Basic statistics
            validation_results['stats']['total_institutions'] = len(institutions_df)
            
            # Check required columns
            required_columns = ['id', 'display_name']
            missing_columns = [col for col in required_columns if col not in institutions_df.columns]
            
            if missing_columns:
                validation_results['errors'].append(f'Missing required columns: {missing_columns}')
                validation_results['valid'] = False
                return validation_results
            
            # Data quality checks
            self._check_data_quality(institutions_df, validation_results, verbose)
            
            # Schema validation
            self._check_schema(institutions_df, validation_results, verbose)
            
            # Geographic data validation
            self._check_geographic_data(institutions_df, validation_results, verbose)
            
            # Rankings validation
            self._check_rankings(institutions_df, validation_results, verbose)
            
            # Search index validation
            if search_index_file.exists():
                self._check_search_index(search_index_file, validation_results, verbose)
            
        except Exception as e:
            validation_results['errors'].append(f'Error during validation: {e}')
            validation_results['valid'] = False
        
        # Final validation status
        if validation_results['errors']:
            validation_results['valid'] = False
        
        return validation_results
    
    def _check_data_quality(self, df, results, verbose):
        """Check data quality metrics."""
        
        # Check for empty records
        empty_names = df.filter(pl.col('display_name').is_null() | (pl.col('display_name') == '')).height
        if empty_names > 0:
            results['warnings'].append(f'{empty_names} institutions have empty names')
        
        # Check for duplicates
        duplicate_ids = df.height - df.n_unique(subset=['id'])
        if duplicate_ids > 0:
            results['errors'].append(f'{duplicate_ids} duplicate institution IDs found')
        
        # Country code validation
        if 'country_code' in df.columns:
            null_countries = df.filter(pl.col('country_code').is_null()).height
            results['stats']['institutions_without_country'] = null_countries
            
            if null_countries > df.height * 0.1:  # More than 10% missing
                results['warnings'].append(f'{null_countries} institutions missing country information')
        
        if verbose:
            self.stdout.write(f"Data quality checks completed")
    
    def _check_schema(self, df, results, verbose):
        """Validate the dataset schema."""
        
        expected_columns = {
            'id': pl.Utf8,
            'display_name': pl.Utf8,
            'canonical_name': pl.Utf8,
            'country_code': pl.Utf8,
            'homepage_url': pl.Utf8,
            'works_count': (pl.Int64, pl.Int32),
            'cited_by_count': (pl.Int64, pl.Int32),
            'webometrics_rank': (pl.Int64, pl.Int32),
        }
        
        for col_name, expected_type in expected_columns.items():
            if col_name in df.columns:
                actual_type = df[col_name].dtype
                
                # Handle multiple acceptable types
                if isinstance(expected_type, tuple):
                    if actual_type not in expected_type:
                        results['warnings'].append(
                            f'Column {col_name} has type {actual_type}, expected one of {expected_type}'
                        )
                else:
                    if actual_type != expected_type:
                        results['warnings'].append(
                            f'Column {col_name} has type {actual_type}, expected {expected_type}'
                        )
        
        results['stats']['columns'] = list(df.columns)
        
        if verbose:
            self.stdout.write(f"Schema validation completed")
    
    def _check_geographic_data(self, df, results, verbose):
        """Validate geographic data."""
        
        if 'geo_latitude' in df.columns and 'geo_longitude' in df.columns:
            # Check for valid coordinate ranges
            invalid_lat = df.filter(
                (pl.col('geo_latitude') < -90) | (pl.col('geo_latitude') > 90)
            ).height
            
            invalid_lon = df.filter(
                (pl.col('geo_longitude') < -180) | (pl.col('geo_longitude') > 180)
            ).height
            
            if invalid_lat > 0:
                results['warnings'].append(f'{invalid_lat} institutions have invalid latitude values')
            
            if invalid_lon > 0:
                results['warnings'].append(f'{invalid_lon} institutions have invalid longitude values')
            
            # Count institutions with geographic data
            with_geo = df.filter(
                pl.col('geo_latitude').is_not_null() & pl.col('geo_longitude').is_not_null()
            ).height
            
            results['stats']['institutions_with_coordinates'] = with_geo
        
        if verbose:
            self.stdout.write(f"Geographic data validation completed")
    
    def _check_rankings(self, df, results, verbose):
        """Validate ranking data."""
        
        if 'webometrics_rank' in df.columns:
            ranked_institutions = df.filter(pl.col('webometrics_rank').is_not_null()).height
            results['stats']['ranked_institutions'] = ranked_institutions
            
            # Check for reasonable ranking values
            if ranked_institutions > 0:
                max_rank = df.select(pl.col('webometrics_rank').max()).item()
                min_rank = df.select(pl.col('webometrics_rank').min()).item()
                
                results['stats']['ranking_range'] = f"{min_rank} to {max_rank}"
                
                # Validate ranking range
                if min_rank < 1:
                    results['warnings'].append(f'Rankings include values less than 1 (min: {min_rank})')
                
                if max_rank > 50000:  # Reasonable upper bound
                    results['warnings'].append(f'Rankings include very high values (max: {max_rank})')
        
        if verbose:
            self.stdout.write(f"Rankings validation completed")
    
    def _check_search_index(self, search_index_file, results, verbose):
        """Validate search index."""
        
        try:
            import polars as pl
            search_df = pl.read_parquet(search_index_file)
            
            required_search_columns = ['id', 'display_name', 'search_tokens']
            missing_search_columns = [col for col in required_search_columns if col not in search_df.columns]
            
            if missing_search_columns:
                results['warnings'].append(f'Search index missing columns: {missing_search_columns}')
            else:
                results['stats']['search_index_entries'] = len(search_df)
            
        except Exception as e:
            results['warnings'].append(f'Error validating search index: {e}')
        
        if verbose:
            self.stdout.write(f"Search index validation completed")
    
    def _print_detailed_stats(self, stats):
        """Print detailed statistics."""
        
        self.stdout.write(self.style.SUCCESS("\nDataset Statistics:"))
        
        for key, value in stats.items():
            formatted_key = key.replace('_', ' ').title()
            self.stdout.write(f"  {formatted_key}: {value}")
        
        self.stdout.write("")
