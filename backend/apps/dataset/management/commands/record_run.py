"""
Django management command to record an ingestion run in the database.

This command creates an IngestionRun record, useful for tracking
external data processing or recording successful operations.

Example usage:
    python manage.py record_run --source openalex --version 2025.09 --status success --stats '{"institutions": 10000}'
"""

import json
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from apps.dataset.models import IngestionRun


class Command(BaseCommand):
    help = 'Record an ingestion run in the database'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--source',
            type=str,
            required=True,
            help='Data source name (e.g., openalex, webometrics, curation)'
        )
        parser.add_argument(
            '--version',
            type=str,
            required=True,
            help='Version identifier (e.g., 2025.09)'
        )
        parser.add_argument(
            '--status',
            type=str,
            choices=['pending', 'running', 'success', 'failed', 'cancelled'],
            required=True,
            help='Status of the ingestion run'
        )
        parser.add_argument(
            '--stats',
            type=str,
            help='JSON string of statistics (e.g., \'{"institutions": 10000}\')'
        )
        parser.add_argument(
            '--error',
            type=str,
            help='Error message if status is failed'
        )
        parser.add_argument(
            '--started-at',
            type=str,
            help='Start time in ISO format (defaults to now)'
        )
        parser.add_argument(
            '--finished-at',
            type=str,
            help='Finish time in ISO format (defaults to now if status is completed)'
        )
        parser.add_argument(
            '--update',
            action='store_true',
            help='Update existing run instead of creating new one'
        )
    
    def handle(self, *args, **options):
        source = options['source']
        version = options['version']
        status = options['status'].upper()
        stats_json = options.get('stats')
        error = options.get('error')
        started_at = options.get('started_at')
        finished_at = options.get('finished_at')
        update = options['update']
        
        # Parse statistics
        stats = {}
        if stats_json:
            try:
                stats = json.loads(stats_json)
            except json.JSONDecodeError as e:
                raise CommandError(f"Invalid JSON in --stats: {e}")
        
        # Parse timestamps
        if started_at:
            try:
                started_at = timezone.datetime.fromisoformat(started_at.replace('Z', '+00:00'))
            except ValueError as e:
                raise CommandError(f"Invalid timestamp format in --started-at: {e}")
        
        if finished_at:
            try:
                finished_at = timezone.datetime.fromisoformat(finished_at.replace('Z', '+00:00'))
            except ValueError as e:
                raise CommandError(f"Invalid timestamp format in --finished-at: {e}")
        elif status in ['SUCCESS', 'FAILED', 'CANCELLED']:
            finished_at = timezone.now()
        
        # Create or update the run
        if update:
            try:
                run = IngestionRun.objects.get(source=source, version=version)
                self.stdout.write(f"Updating existing run: {source} {version}")
                
                # Update fields
                run.status = status
                if stats:
                    run.stats.update(stats)
                if error:
                    run.error = error
                if started_at:
                    run.started_at = started_at
                if finished_at:
                    run.finished_at = finished_at
                
                run.save()
                
            except IngestionRun.DoesNotExist:
                raise CommandError(f"Run not found: {source} {version}. Use without --update to create.")
                
        else:
            # Check if run already exists
            if IngestionRun.objects.filter(source=source, version=version).exists():
                raise CommandError(
                    f"Run already exists: {source} {version}. Use --update to modify existing run."
                )
            
            self.stdout.write(f"Creating new run: {source} {version}")
            
            run = IngestionRun.objects.create(
                source=source,
                version=version,
                status=status,
                stats=stats,
                error=error or '',
                finished_at=finished_at
            )
            
            # Update started_at if provided
            if started_at:
                run.started_at = started_at
                run.save()
        
        # Display run information
        self.stdout.write(self.style.SUCCESS(f"Successfully recorded ingestion run:"))
        self.stdout.write(f"  ID: {run.id}")
        self.stdout.write(f"  Source: {run.source}")
        self.stdout.write(f"  Version: {run.version}")
        self.stdout.write(f"  Status: {run.status}")
        self.stdout.write(f"  Started: {run.started_at}")
        self.stdout.write(f"  Finished: {run.finished_at}")
        
        if run.stats:
            self.stdout.write(f"  Statistics:")
            for key, value in run.stats.items():
                self.stdout.write(f"    {key}: {value}")
        
        if run.error:
            self.stdout.write(f"  Error: {run.error}")
        
        if run.duration_seconds:
            self.stdout.write(f"  Duration: {run.duration_seconds:.1f} seconds")
