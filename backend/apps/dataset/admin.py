from django.contrib import admin
from .models import IngestionRun


@admin.register(IngestionRun)
class IngestionRunAdmin(admin.ModelAdmin):
    list_display = ('source', 'version', 'status', 'started_at', 'finished_at')
    list_filter = ('source', 'status', 'started_at')
    search_fields = ('source', 'version')
    readonly_fields = ('started_at', 'finished_at')
    ordering = ('-started_at',)
