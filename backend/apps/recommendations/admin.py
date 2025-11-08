from django.contrib import admin
from .models import Recommendation


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ('user', 'university_ref', 'program', 'score', 'generated_at')
    list_filter = ('generated_at', 'program')
    search_fields = ('user__email', 'university_ref', 'program')
    readonly_fields = ('generated_at',)
    ordering = ('-generated_at', '-score')
