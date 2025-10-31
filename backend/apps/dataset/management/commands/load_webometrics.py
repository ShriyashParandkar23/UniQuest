"""
Django management command to load Webometrics ranking data.

Example usage:
    python manage.py load_webometrics --version 2025.09 --csv /data/raw/webometrics/2025.09/webometrics.csv
"""

import csv
import json
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.utils import timezone
from apps.dataset.models import IngestionRun


class Command(BaseCommand):
    help = 'Load Webometrics ranking data from CSV file'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--version',
            type=str,
            required=True,
            help='Version identifier for the dataset (e.g., 2025.09)'
        )
        parser.add_argument(
            '--csv',
            type=str,
            required=True,
            help='Path to Webometrics CSV file'
        )
        parser.add_argument(
            '--output-dir',
            type=str,
            help='Output directory for processed data'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be processed without actually processing'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force processing even if data already exists'
        )
    
    def handle(self, *args, **options):
        version = options['version']
        csv_file = Path(options['csv'])
        dry_run = options['dry_run']
        force = options['force']
        
        # Validate CSV file exists
        if not csv_file.exists():
            raise CommandError(f"CSV file not found: {csv_file}")
        
        # Set up output directory
        if options['output_dir']:
            output_dir = Path(options['output_dir'])
        else:
            base_path = Path(getattr(settings, 'DATASET_BASE_PATH', '/data'))
            output_dir = base_path / 'raw' / 'webometrics' / version
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        self.stdout.write(f"Loading Webometrics data version {version}")
        self.stdout.write(f"Input CSV: {csv_file}")
        self.stdout.write(f"Output directory: {output_dir}")
        
        if dry_run:
            self.stdout.write(self.style.WARNING("DRY RUN - No data will be processed"))
            self._analyze_csv(csv_file)
            return
        
        # Check if data already exists
        output_file = output_dir / 'webometrics.jsonl'
        if output_file.exists() and not force:
            raise CommandError(
                f"Data already exists at {output_file}. Use --force to overwrite."
            )
        
        # Create ingestion run record
        run = IngestionRun.objects.create(
            source='webometrics',
            version=version,
            status='RUNNING'
        )
        
        try:
            # Process the CSV file
            self._process_csv(csv_file, output_file, run)
            
            # Mark run as successful
            run.status = 'SUCCESS'
            run.finished_at = timezone.now()
            run.save()
            
            self.stdout.write(
                self.style.SUCCESS(f"Successfully processed Webometrics data version {version}")
            )
            
        except Exception as e:
            # Mark run as failed
            run.status = 'FAILED'
            run.error = str(e)
            run.finished_at = timezone.now()
            run.save()
            
            raise CommandError(f"Processing failed: {e}")
    
    def _analyze_csv(self, csv_file):
        """Analyze the CSV file structure (for dry run)."""
        self.stdout.write("Analyzing CSV file structure...")
        
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)
            
            self.stdout.write(f"Headers found: {headers}")
            
            # Read a few sample rows
            sample_rows = []
            for i, row in enumerate(reader):
                if i >= 5:  # Just read first 5 rows
                    break
                sample_rows.append(row)
            
            self.stdout.write(f"Sample data (first 5 rows):")
            for i, row in enumerate(sample_rows):
                self.stdout.write(f"  Row {i+1}: {row[:3]}...")  # Show first 3 columns
    
    def _process_csv(self, csv_file, output_file, run):
        """Process the Webometrics CSV file."""
        
        processed_count = 0
        
        with open(csv_file, 'r', encoding='utf-8') as infile, \
             open(output_file, 'w', encoding='utf-8') as outfile:
            
            reader = csv.DictReader(infile)
            
            # Expected column mappings (adjust based on actual CSV format)
            column_mappings = {
                'Ranking': 'rank',
                'University': 'name',
                'Det': 'details',
                'Presence Rank': 'presence_rank',
                'Impact Rank': 'impact_rank',
                'Openness Rank': 'openness_rank',
                'Excellence Rank': 'excellence_rank',
                'Country': 'country',
            }
            
            for row in reader:
                try:
                    # Create standardized record
                    record = {
                        'source': 'webometrics',
                        'version': run.version,
                    }
                    
                    # Map CSV columns to our schema
                    for csv_col, our_field in column_mappings.items():
                        if csv_col in row:
                            value = row[csv_col].strip()
                            
                            # Convert numeric fields
                            if 'rank' in our_field or 'Rank' in csv_col:
                                try:
                                    record[our_field] = int(value) if value else None
                                except ValueError:
                                    record[our_field] = None
                            else:
                                record[our_field] = value if value else None
                    
                    # Create a canonical name for matching
                    if 'name' in record and record['name']:
                        record['canonical_name'] = self._create_canonical_name(record['name'])
                    
                    # Extract homepage URL if available in details
                    if 'details' in record and record['details']:
                        record['homepage_url'] = self._extract_homepage(record['details'])
                    
                    outfile.write(json.dumps(record) + '\n')
                    processed_count += 1
                    
                    if processed_count % 100 == 0:
                        self.stdout.write(f"Processed {processed_count} records...")
                        
                        # Update run statistics
                        run.set_stat('processed_count', processed_count)
                        run.save()
                
                except Exception as e:
                    self.stdout.write(
                        self.style.WARNING(f"Error processing row {processed_count + 1}: {e}")
                    )
                    continue
        
        self.stdout.write(f"Processed {processed_count} records total")
        
        # Final statistics
        run.set_stat('total_records', processed_count)
        run.save()
    
    def _create_canonical_name(self, name):
        """Create a canonical name for matching with OpenAlex data."""
        if not name:
            return ''
        
        import re
        
        # Remove common prefixes and suffixes
        canonical = name.lower()
        canonical = re.sub(r'^(university of |the |)', '', canonical)
        canonical = re.sub(r'( university| college| institute| school)$', '', canonical)
        
        # Remove special characters and normalize spaces
        canonical = re.sub(r'[^\w\s-]', '', canonical)
        canonical = re.sub(r'\s+', '-', canonical.strip())
        
        return canonical
    
    def _extract_homepage(self, details):
        """Extract homepage URL from details field."""
        import re
        
        # Look for URL patterns in the details
        url_pattern = r'https?://[^\s<>"]+\.[^\s<>"]+'
        match = re.search(url_pattern, details)
        
        if match:
            return match.group(0)
        
        return None
