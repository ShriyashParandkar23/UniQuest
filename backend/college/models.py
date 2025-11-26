from django.db import models

class College(models.Model):
    world_rank = models.IntegerField()
    institution = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    national_rank = models.IntegerField(null=True, blank=True)
    quality_of_education = models.FloatField(null=True, blank=True)
    alumni_employment = models.FloatField(null=True, blank=True)
    quality_of_faculty = models.FloatField(null=True, blank=True)
    publications = models.FloatField(null=True, blank=True)
    influence = models.FloatField(null=True, blank=True)
    citations = models.FloatField(null=True, blank=True)
    broad_impact = models.FloatField(null=True, blank=True)
    patents = models.FloatField(null=True, blank=True)
    score = models.FloatField(null=True, blank=True)
    year = models.IntegerField()

    def __str__(self):
        return f"{self.institution} ({self.country}) - World Rank: {self.world_rank}"
