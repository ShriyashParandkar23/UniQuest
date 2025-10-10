from django.db import models


class IngestionRun(models.Model):
    """Metadata for dataset ingestion runs."""
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('RUNNING', 'Running'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    source = models.CharField(
        max_length=100,
        help_text="Data source name (e.g., 'openalex', 'webometrics')"
    )
    
    version = models.CharField(
        max_length=50,
        help_text="Version identifier (e.g., '2025.09')"
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    
    stats = models.JSONField(
        default=dict,
        blank=True,
        help_text="Statistics about the ingestion run"
    )
    
    error = models.TextField(
        blank=True,
        help_text="Error message if the run failed"
    )
    
    class Meta:
        db_table = 'ingestion_runs'
        unique_together = ['source', 'version']
        indexes = [
            models.Index(fields=['source', 'version']),
            models.Index(fields=['status']),
            models.Index(fields=['-started_at']),
        ]
        ordering = ['-started_at']
    
    def __str__(self):
        return f"{self.source} {self.version} ({self.status})"
    
    @property
    def duration_seconds(self):
        """Return duration in seconds if finished."""
        if self.finished_at and self.started_at:
            delta = self.finished_at - self.started_at
            return delta.total_seconds()
        return None
    
    @property
    def is_completed(self):
        """Return True if the run is completed (success or failed)."""
        return self.status in ['SUCCESS', 'FAILED', 'CANCELLED']
    
    def get_stat(self, stat_name, default=None):
        """Get a specific statistic."""
        return self.stats.get(stat_name, default)
    
    def set_stat(self, stat_name, value):
        """Set a specific statistic."""
        if not self.stats:
            self.stats = {}
        self.stats[stat_name] = value
