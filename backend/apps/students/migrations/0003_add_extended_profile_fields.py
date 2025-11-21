# Generated manually for extended profile fields
# Migration to add: academic_level, academic_background, work_experience,
# preferred_programs, preferred_countries, campus_preference, budget_currency
# and update test_scores to array format

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentprofile',
            name='academic_level',
            field=models.CharField(
                blank=True,
                choices=[
                    ('high-school', 'High School'),
                    ('bachelors', "Bachelor's Degree"),
                    ('masters', "Master's Degree"),
                    ('phd', 'PhD'),
                    ('other', 'Other'),
                ],
                help_text='Current or target academic level',
                max_length=20,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='academic_background',
            field=models.JSONField(
                blank=True,
                default=list,
                help_text='Array of academic background entries with level, course, institution, year_of_completion, gpa',
            ),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='work_experience',
            field=models.JSONField(
                blank=True,
                default=list,
                help_text='Array of work experience entries',
            ),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='preferred_programs',
            field=models.JSONField(
                blank=True,
                default=list,
                help_text='Array of preferred academic programs/fields of study',
            ),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='preferred_countries',
            field=models.JSONField(
                blank=True,
                default=list,
                help_text='Array of preferred countries (full names or ISO codes)',
            ),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='campus_preference',
            field=models.JSONField(
                blank=True,
                default=list,
                help_text='Array of campus preferences (Urban, Suburban, Rural)',
            ),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='budget_currency',
            field=models.CharField(
                blank=True,
                default='USD',
                help_text='ISO 3-letter currency code (e.g., USD, EUR, GBP)',
                max_length=3,
            ),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='test_scores',
            field=models.JSONField(
                blank=True,
                default=list,
                help_text='Array of test scores with exam_name, score, test_date',
            ),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='budget_max',
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                help_text='Maximum budget (maxTuition)',
                max_digits=10,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='budget_min',
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                help_text='Minimum budget',
                max_digits=10,
                null=True,
            ),
        ),
    ]

