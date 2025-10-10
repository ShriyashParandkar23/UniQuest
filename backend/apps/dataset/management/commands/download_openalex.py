"""
Django management command to download university data from Kaggle.

Example usage:
    python manage.py download_dataset --version 2025.09 --kaggle-dataset "username/dataset-name" --output-dir /data/raw/kaggle/2025.09
"""

import os
import requests
import json
import zipfile
import pandas as pd
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.utils import timezone
from apps.dataset.models import IngestionRun


class Command(BaseCommand):
    help = 'Download university data from Kaggle dataset'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--version',
            type=str,
            required=True,
            help='Version identifier for the dataset (e.g., 2025.09)'
        )
        parser.add_argument(
            '--kaggle-dataset',
            type=str,
            required=True,
            help='Kaggle dataset identifier (e.g., "username/dataset-name")'
        )
        parser.add_argument(
            '--output-dir',
            type=str,
            help='Output directory for downloaded data'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be downloaded without actually downloading'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force download even if data already exists'
        )
    
    def handle(self, *args, **options):
        version = options['version']
        kaggle_dataset = options['kaggle_dataset']
        dry_run = options['dry_run']
        force = options['force']
        
        # Set up output directory
        if options['output_dir']:
            output_dir = Path(options['output_dir'])
        else:
            base_path = Path(getattr(settings, 'DATASET_BASE_PATH', './data'))
            output_dir = base_path / 'raw' / 'kaggle' / version
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        self.stdout.write(f"Downloading Kaggle dataset: {kaggle_dataset}")
        self.stdout.write(f"Version: {version}")
        self.stdout.write(f"Output directory: {output_dir}")
        
        if dry_run:
            self.stdout.write(self.style.WARNING("DRY RUN - No data will be downloaded"))
            self.stdout.write(f"Would download from: https://www.kaggle.com/datasets/{kaggle_dataset}")
            return
        
        # Check if data already exists  
        institutions_file = output_dir / 'institutions.csv'
        if institutions_file.exists() and not force:
            raise CommandError(
                f"Data already exists at {institutions_file}. Use --force to overwrite."
            )
        
        # Create ingestion run record
        run = IngestionRun.objects.create(
            source='kaggle',
            version=version,
            status='RUNNING'
        )
        
        try:
            # Download Kaggle dataset
            self._download_kaggle_dataset(kaggle_dataset, output_dir, run)
            
            # Mark run as successful
            run.status = 'SUCCESS'
            run.finished_at = timezone.now()
            run.save()
            
            self.stdout.write(
                self.style.SUCCESS(f"Successfully downloaded Kaggle dataset {kaggle_dataset} version {version}")
            )
            
        except Exception as e:
            # Mark run as failed
            run.status = 'FAILED'
            run.error = str(e)
            run.finished_at = timezone.now()
            run.save()
            
            raise CommandError(f"Download failed: {e}")
    
    def _download_kaggle_dataset(self, kaggle_dataset, output_dir, run):
        """Download and process Kaggle dataset."""
        
        # Construct Kaggle dataset URL
        kaggle_url = f"https://www.kaggle.com/api/v1/datasets/download/{kaggle_dataset}"
        
        self.stdout.write(f"Downloading from Kaggle: {kaggle_url}")
        
        # Download the dataset
        try:
            # Note: This requires Kaggle API authentication
            # Users need to set up their Kaggle API credentials
            headers = {}
            
            # Try to get Kaggle credentials from environment
            kaggle_username = os.environ.get('KAGGLE_USERNAME')
            kaggle_key = os.environ.get('KAGGLE_KEY')
            
            if kaggle_username and kaggle_key:
                import base64
                credentials = base64.b64encode(f"{kaggle_username}:{kaggle_key}".encode()).decode()
                headers['Authorization'] = f'Basic {credentials}'
            
            response = requests.get(kaggle_url, headers=headers, timeout=300)
            
            if response.status_code == 401:
                raise CommandError(
                    "Kaggle authentication failed. Please set KAGGLE_USERNAME and KAGGLE_KEY "
                    "environment variables or provide a direct dataset URL."
                )
            
            response.raise_for_status()
            
            # Save the zip file
            zip_file_path = output_dir / 'dataset.zip'
            with open(zip_file_path, 'wb') as f:
                f.write(response.content)
            
            self.stdout.write(f"Downloaded dataset zip file: {zip_file_path}")
            
            # Extract the zip file
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(output_dir)
            
            # Remove the zip file
            zip_file_path.unlink()
            
            # Find CSV files and process them
            csv_files = list(output_dir.glob('*.csv'))
            
            if not csv_files:
                raise CommandError("No CSV files found in the downloaded dataset")
            
            # Process the main dataset file
            main_csv = csv_files[0]  # Use the first CSV file found
            self.stdout.write(f"Processing CSV file: {main_csv}")
            
            # Read and process the CSV
            df = pd.read_csv(main_csv)
            processed_count = self._process_university_data(df, output_dir, run)
            
            # Update run statistics
            run.set_stat('total_institutions', processed_count)
            run.set_stat('source_file', str(main_csv))
            run.save()
            
        except requests.RequestException as e:
            raise CommandError(f"Failed to download from Kaggle: {e}")
        except Exception as e:
            raise CommandError(f"Error processing dataset: {e}")
    
    def _process_university_data(self, df, output_dir, run):
        """Process the university dataset and standardize format."""
        
        institutions_file = output_dir / 'institutions.csv'
        processed_count = 0
        
        # Define column mappings (common variations)
        column_mappings = {
            'name': ['name', 'university_name', 'institution_name', 'school_name', 'college_name'],
            'country': ['country', 'country_code', 'nation', 'location_country'],
            'ranking': ['ranking', 'rank', 'world_rank', 'global_rank'],
            'website': ['website', 'homepage', 'url', 'homepage_url'],
            'location': ['location', 'city', 'state', 'region'],
        }
        
        # Create standardized DataFrame
        standardized_data = []
        
        for index, row in df.iterrows():
            institution = {
                'id': f"kaggle_{kaggle_dataset.replace('/', '_')}_{index}",
                'display_name': '',
                'canonical_name': '',
                'country_code': '',
                'homepage_url': '',
                'webometrics_rank': None,
                'works_count': 0,
                'cited_by_count': 0,
                'geo_latitude': None,
                'geo_longitude': None,
            }
            
            # Map columns to standardized format
            for col in df.columns:
                col_lower = col.lower()
                
                # Name mapping
                if any(name_var in col_lower for name_var in column_mappings['name']):
                    institution['display_name'] = str(row[col])
                    institution['canonical_name'] = self._create_canonical_name(str(row[col]))
                
                # Country mapping
                elif any(country_var in col_lower for country_var in column_mappings['country']):
                    country_val = str(row[col])
                    if len(country_val) == 2:
                        institution['country_code'] = country_val.upper()
                    else:
                        institution['country_code'] = self._country_to_code(country_val)
                
                # Ranking mapping
                elif any(rank_var in col_lower for rank_var in column_mappings['ranking']):
                    try:
                        institution['webometrics_rank'] = int(float(str(row[col])))
                    except (ValueError, TypeError):
                        pass
                
                # Website mapping
                elif any(web_var in col_lower for web_var in column_mappings['website']):
                    website = str(row[col])
                    if website and website != 'nan' and website.startswith('http'):
                        institution['homepage_url'] = website
            
            if institution['display_name']:  # Only add if we have a name
                standardized_data.append(institution)
                processed_count += 1
        
        # Save standardized data
        standardized_df = pd.DataFrame(standardized_data)
        standardized_df.to_csv(institutions_file, index=False)
        
        self.stdout.write(f"Processed {processed_count} institutions")
        
        return processed_count
    
    def _create_canonical_name(self, display_name):
        """Create a canonical name for searching."""
        if not display_name:
            return ''
        
        # Simple canonicalization - remove special chars, lowercase
        import re
        canonical = re.sub(r'[^\w\s-]', '', display_name.lower())
        canonical = re.sub(r'\s+', '-', canonical.strip())
        return canonical
    
    def _country_to_code(self, country_name):
        """Convert country name to 2-letter code."""
        # Basic country name to code mapping
        country_codes = {
            'united states': 'US',
            'usa': 'US',
            'america': 'US',
            'united kingdom': 'GB',
            'uk': 'GB',
            'canada': 'CA',
            'australia': 'AU',
            'germany': 'DE',
            'france': 'FR',
            'italy': 'IT',
            'spain': 'ES',
            'netherlands': 'NL',
            'sweden': 'SE',
            'norway': 'NO',
            'denmark': 'DK',
            'finland': 'FI',
            'switzerland': 'CH',
            'austria': 'AT',
            'belgium': 'BE',
            'japan': 'JP',
            'china': 'CN',
            'india': 'IN',
            'south korea': 'KR',
            'singapore': 'SG',
            'hong kong': 'HK',
            'brazil': 'BR',
            'mexico': 'MX',
            'argentina': 'AR',
            'chile': 'CL',
            'south africa': 'ZA',
            'israel': 'IL',
            'russia': 'RU',
            'poland': 'PL',
            'czech republic': 'CZ',
            'hungary': 'HU',
            'turkey': 'TR',
            'greece': 'GR',
            'portugal': 'PT',
            'ireland': 'IE',
            'new zealand': 'NZ',
        }
        
        country_lower = country_name.lower().strip()
        return country_codes.get(country_lower, country_lower[:2].upper())
