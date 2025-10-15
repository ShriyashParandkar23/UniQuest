"""
Django management command to curate and merge dataset sources.

This command:
1. Merges OpenAlex institutions with Webometrics rankings
2. Creates normalized and searchable dataset
3. Builds search index for fast queries
4. Outputs final Parquet files

Example usage:
    python manage.py curate --version 2025.09
"""

import json
import pandas as pd
import polars as pl
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.utils import timezone
from apps.dataset.models import IngestionRun


class Command(BaseCommand):
    help = 'Curate and merge dataset sources into final format'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--version',
            type=str,
            required=True,
            help='Version identifier for the dataset (e.g., 2025.09)'
        )
        parser.add_argument(
            '--input-dir',
            type=str,
            help='Input directory containing raw data'
        )
        parser.add_argument(
            '--output-dir',
            type=str,
            help='Output directory for curated data'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be processed without actually processing'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force curation even if data already exists'
        )
    
    def handle(self, *args, **options):
        version = options['version']
        dry_run = options['dry_run']
        force = options['force']
        
        base_path = Path(getattr(settings, 'DATASET_BASE_PATH', '/data'))
        
        # Set up directories
        if options['input_dir']:
            input_dir = Path(options['input_dir'])
        else:
            input_dir = base_path / 'raw'
        
        if options['output_dir']:
            output_dir = Path(options['output_dir'])
        else:
            output_dir = base_path / 'curated' / version
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        self.stdout.write(f"Curating dataset version {version}")
        self.stdout.write(f"Input directory: {input_dir}")
        self.stdout.write(f"Output directory: {output_dir}")
        
        if dry_run:
            self.stdout.write(self.style.WARNING("DRY RUN - No data will be processed"))
            self._analyze_inputs(input_dir, version)
            return
        
        # Check if data already exists
        institutions_file = output_dir / 'institutions.parquet'
        if institutions_file.exists() and not force:
            raise CommandError(
                f"Curated data already exists at {institutions_file}. Use --force to overwrite."
            )
        
        # Create ingestion run record
        run = IngestionRun.objects.create(
            source='curation',
            version=version,
            status='RUNNING'
        )
        
        try:
            # Load and process data
            institutions_df = self._curate_data(input_dir, version, run)
            
            # Save as Parquet
            self._save_parquet(institutions_df, output_dir, run)
            
            # Create search index
            self._create_search_index(institutions_df, output_dir, run)
            
            # Mark run as successful
            run.status = 'SUCCESS'
            run.finished_at = timezone.now()
            run.save()
            
            self.stdout.write(
                self.style.SUCCESS(f"Successfully curated dataset version {version}")
            )
            
        except Exception as e:
            # Mark run as failed
            run.status = 'FAILED'
            run.error = str(e)
            run.finished_at = timezone.now()
            run.save()
            
            raise CommandError(f"Curation failed: {e}")
    
    def _analyze_inputs(self, input_dir, version):
        """Analyze input files (for dry run)."""
        self.stdout.write("Analyzing input files...")
        
        # Check Kaggle data
        kaggle_file = input_dir / 'kaggle' / version / 'institutions.csv'
        if kaggle_file.exists():
            import pandas as pd
            df = pd.read_csv(kaggle_file)
            line_count = len(df)
            self.stdout.write(f"Kaggle institutions: {line_count} records")
        else:
            self.stdout.write(self.style.WARNING(f"Kaggle data not found: {kaggle_file}"))
        
        # Check Webometrics data
        webometrics_file = input_dir / 'webometrics' / version / 'webometrics.jsonl'
        if webometrics_file.exists():
            with open(webometrics_file, 'r') as f:
                line_count = sum(1 for _ in f)
            self.stdout.write(f"Webometrics rankings: {line_count} records")
        else:
            self.stdout.write(self.style.WARNING(f"Webometrics data not found: {webometrics_file}"))
    
    def _curate_data(self, input_dir, version, run):
        """Load and curate the data."""
        
        # Load Kaggle institutions
        self.stdout.write("Loading Kaggle dataset institutions...")
        kaggle_file = input_dir / 'kaggle' / version / 'institutions.csv'
        
        if not kaggle_file.exists():
            raise CommandError(f"Kaggle data not found: {kaggle_file}")
        
        # Use Polars for efficient data processing
        institutions_df = pl.read_csv(kaggle_file)
        
        self.stdout.write(f"Loaded {len(institutions_df)} Kaggle institutions")
        
        # Clean and normalize the data
        institutions_df = self._clean_institutions(institutions_df)
        
        # Load Webometrics rankings (optional)
        webometrics_file = input_dir / 'webometrics' / version / 'webometrics.jsonl'
        
        if webometrics_file.exists():
            self.stdout.write("Loading Webometrics rankings...")
            webometrics_df = pl.read_ndjson(webometrics_file)
            
            self.stdout.write(f"Loaded {len(webometrics_df)} Webometrics rankings")
            
            # Merge with rankings
            institutions_df = self._merge_rankings(institutions_df, webometrics_df)
        else:
            self.stdout.write("Webometrics data not found, skipping rankings merge")
        
        # Update run statistics
        run.set_stat('total_institutions', len(institutions_df))
        ranked_count = institutions_df.filter(pl.col('webometrics_rank').is_not_null()).height
        run.set_stat('ranked_institutions', ranked_count)
        run.save()
        
        return institutions_df
    
    def _clean_institutions(self, df):
        """Clean and normalize institutions data."""
        
        # Extract geographic coordinates
        df = df.with_columns([
            pl.col('geo').map_elements(lambda x: x.get('latitude') if isinstance(x, dict) else None).alias('geo_latitude'),
            pl.col('geo').map_elements(lambda x: x.get('longitude') if isinstance(x, dict) else None).alias('geo_longitude'),
        ])
        
        # Create search-friendly name
        df = df.with_columns([
            pl.col('display_name').fill_null('').alias('display_name'),
            pl.col('canonical_name').fill_null('').alias('canonical_name'),
        ])
        
        # Ensure numeric fields are properly typed
        df = df.with_columns([
            pl.col('works_count').cast(pl.Int64, strict=False).fill_null(0),
            pl.col('cited_by_count').cast(pl.Int64, strict=False).fill_null(0),
        ])
        
        # Create a normalized name for matching
        df = df.with_columns([
            pl.col('display_name').map_elements(self._normalize_name).alias('normalized_name')
        ])
        
        return df
    
    def _merge_rankings(self, institutions_df, webometrics_df):
        """Merge institutions with Webometrics rankings."""
        
        # Normalize names in webometrics data for matching
        webometrics_df = webometrics_df.with_columns([
            pl.col('name').map_elements(self._normalize_name).alias('normalized_name')
        ])
        
        # Perform fuzzy matching join
        # For now, use exact match on normalized names
        merged_df = institutions_df.join(
            webometrics_df.select(['normalized_name', 'rank', 'country']),
            on='normalized_name',
            how='left',
            suffix='_webometrics'
        )
        
        # Rename webometrics rank column
        merged_df = merged_df.rename({'rank': 'webometrics_rank'})
        
        # Update country code if missing from OpenAlex but available in Webometrics
        merged_df = merged_df.with_columns([
            pl.when(pl.col('country_code').is_null() & pl.col('country_webometrics').is_not_null())
            .then(pl.col('country_webometrics'))
            .otherwise(pl.col('country_code'))
            .alias('country_code')
        ])
        
        # Drop temporary columns
        merged_df = merged_df.drop(['country_webometrics'])
        
        return merged_df
    
    def _normalize_name(self, name):
        """Normalize institution name for matching."""
        if not name:
            return ''
        
        import re
        
        # Convert to lowercase
        normalized = name.lower()
        
        # Remove common prefixes and suffixes
        normalized = re.sub(r'^(the |university of |)', '', normalized)
        normalized = re.sub(r'( university| college| institute| school| tech| technological)$', '', normalized)
        
        # Remove special characters
        normalized = re.sub(r'[^\w\s]', '', normalized)
        
        # Normalize whitespace
        normalized = re.sub(r'\s+', ' ', normalized.strip())
        
        return normalized
    
    def _save_parquet(self, df, output_dir, run):
        """Save the curated data as Parquet files."""
        
        institutions_file = output_dir / 'institutions.parquet'
        
        self.stdout.write(f"Saving institutions to {institutions_file}")
        
        # Select final columns
        final_columns = [
            'id', 'display_name', 'canonical_name', 'country_code',
            'homepage_url', 'image_url', 'works_count', 'cited_by_count',
            'geo_latitude', 'geo_longitude', 'type', 'webometrics_rank'
        ]
        
        # Filter to only existing columns
        available_columns = [col for col in final_columns if col in df.columns]
        
        df_final = df.select(available_columns)
        df_final.write_parquet(institutions_file)
        
        self.stdout.write(f"Saved {len(df_final)} institutions to Parquet")
        
        # Update run statistics
        run.set_stat('output_file_size', institutions_file.stat().st_size)
        run.save()
    
    def _create_search_index(self, df, output_dir, run):
        """Create a search index for faster text queries."""
        
        search_index_file = output_dir / 'search_index.parquet'
        
        self.stdout.write(f"Creating search index at {search_index_file}")
        
        # Create search tokens from institution names
        search_df = df.select([
            'id',
            'display_name',
            'canonical_name',
            'country_code',
        ]).with_columns([
            # Create searchable tokens
            pl.col('display_name').map_elements(self._create_search_tokens).alias('search_tokens')
        ])
        
        search_df.write_parquet(search_index_file)
        
        self.stdout.write(f"Created search index with {len(search_df)} entries")
    
    def _create_search_tokens(self, name):
        """Create search tokens from institution name."""
        if not name:
            return []
        
        import re
        
        # Split into words and create variants
        tokens = []
        
        # Original words
        words = re.findall(r'\b\w+\b', name.lower())
        tokens.extend(words)
        
        # Acronyms (first letters)
        if len(words) > 1:
            acronym = ''.join(word[0] for word in words)
            tokens.append(acronym)
        
        # Remove duplicates
        return list(set(tokens))
