"""
Demo data creation script for UniQuest.

This script creates sample users, profiles, and data for demonstration purposes.
Run with: python create_demo_data.py
"""

import os
import sys
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.dev')
django.setup()

import json
from django.contrib.auth import get_user_model
from apps.students.models import StudentProfile
from apps.preferences.models import Preference
from apps.recommendations.models import Recommendation
from apps.feedback.models import Feedback
from apps.dataset.models import IngestionRun

User = get_user_model()

print("Creating demo data for UniQuest...")

# Create demo users
demo_users_data = [
    {
        'email': 'alice@example.com',
        'username': 'alice',
        'first_name': 'Alice',
        'last_name': 'Johnson',
        'password': 'demo123',
        'profile': {
            'gpa': 3.8,
            'interests': 'Computer Science, Machine Learning, Data Science',
            'goals': 'Pursue PhD in AI and work in tech industry',
            'country_preference': 'US',
            'budget_min': 30000,
            'budget_max': 80000,
            'test_scores': {'GRE': 325, 'TOEFL': 108},
            'preferred_regions': ['North America', 'Europe']
        },
        'weights': {
            'academics': 0.4,
            'research_activity': 0.3,
            'ranking': 0.15,
            'location': 0.1,
            'career': 0.05
        }
    },
    {
        'email': 'bob@example.com',
        'username': 'bob',
        'first_name': 'Bob',
        'last_name': 'Smith',
        'password': 'demo123',
        'profile': {
            'gpa': 3.5,
            'interests': 'Engineering, Robotics, Innovation',
            'goals': 'Master\'s in Engineering and startup founder',
            'country_preference': 'CA',
            'budget_min': 20000,
            'budget_max': 60000,
            'test_scores': {'GRE': 315, 'TOEFL': 95},
            'preferred_regions': ['North America']
        },
        'weights': {
            'academics': 0.3,
            'career': 0.3,
            'location': 0.2,
            'budget': 0.15,
            'ranking': 0.05
        }
    },
    {
        'email': 'carol@example.com',
        'username': 'carol',
        'first_name': 'Carol',
        'last_name': 'Davis',
        'password': 'demo123',
        'profile': {
            'gpa': 3.9,
            'interests': 'Medicine, Research, Global Health',
            'goals': 'MD-PhD and medical research career',
            'country_preference': 'GB',
            'budget_min': 40000,
            'budget_max': 100000,
            'test_scores': {'MCAT': 520, 'TOEFL': 115},
            'preferred_regions': ['Europe', 'North America']
        },
        'weights': {
            'academics': 0.5,
            'research_activity': 0.25,
            'ranking': 0.2,
            'location': 0.05
        }
    }
]

created_users = []

for user_data in demo_users_data:
    # Create or get user
    user, created = User.objects.get_or_create(
        email=user_data['email'],
        defaults={
            'username': user_data['username'],
            'first_name': user_data['first_name'],
            'last_name': user_data['last_name'],
            'is_verified': True
        }
    )
    
    if created:
        user.set_password(user_data['password'])
        user.save()
        print(f"Created user: {user.email}")
    else:
        print(f"User already exists: {user.email}")
    
    # Create or update student profile
    profile, profile_created = StudentProfile.objects.get_or_create(
        user=user,
        defaults=user_data['profile']
    )
    
    if profile_created:
        print(f"Created profile for: {user.email}")
    
    # Create or update preferences
    preferences, pref_created = Preference.objects.get_or_create(
        user=user,
        defaults={'weights': user_data['weights']}
    )
    
    if pref_created:
        print(f"Created preferences for: {user.email}")
    
    created_users.append(user)

# Create sample ingestion runs
sample_runs = [
    {
        'source': 'openalex',
        'version': '2025.09',
        'status': 'SUCCESS',
        'stats': {
            'total_institutions': 12543,
            'downloaded_count': 12543,
            'processing_time': 1850
        }
    },
    {
        'source': 'webometrics',
        'version': '2025.09',
        'status': 'SUCCESS',
        'stats': {
            'total_records': 3000,
            'matched_institutions': 2847,
            'processing_time': 120
        }
    },
    {
        'source': 'curation',
        'version': '2025.09',
        'status': 'SUCCESS',
        'stats': {
            'final_institutions': 12543,
            'with_rankings': 2847,
            'with_coordinates': 8934,
            'processing_time': 95
        }
    }
]

for run_data in sample_runs:
    run, created = IngestionRun.objects.get_or_create(
        source=run_data['source'],
        version=run_data['version'],
        defaults={
            'status': run_data['status'],
            'stats': run_data['stats']
        }
    )
    
    if created:
        print(f"Created ingestion run: {run.source} {run.version}")

# Create sample recommendations for Alice
alice = created_users[0]
sample_recommendations = [
    {
        'university_ref': 'https://openalex.org/I97018004',
        'program': 'Computer Science PhD',
        'score': 0.92,
        'rationale': 'Stanford University is highly recommended because: Strong global ranking (#5); High research activity and publication output; Located in preferred region (US). Overall match score: 92%.',
        'filters': {'country': 'US', 'has_research': True},
        'weights': {'academics': 0.4, 'research_activity': 0.3, 'ranking': 0.15, 'location': 0.1, 'career': 0.05}
    },
    {
        'university_ref': 'https://openalex.org/I136199984',
        'program': 'Computer Science PhD',
        'score': 0.89,
        'rationale': 'Massachusetts Institute of Technology is recommended because: Strong global ranking (#3); High research activity and publication output; Located in preferred region (US). Overall match score: 89%.',
        'filters': {'country': 'US', 'has_research': True},
        'weights': {'academics': 0.4, 'research_activity': 0.3, 'ranking': 0.15, 'location': 0.1, 'career': 0.05}
    },
    {
        'university_ref': 'https://openalex.org/I114027177',
        'program': 'Computer Science PhD',
        'score': 0.85,
        'rationale': 'Carnegie Mellon University is recommended because: Strong academic programs matching your profile; High research activity and publication output; Located in preferred region (US). Overall match score: 85%.',
        'filters': {'country': 'US', 'has_research': True},
        'weights': {'academics': 0.4, 'research_activity': 0.3, 'ranking': 0.15, 'location': 0.1, 'career': 0.05}
    }
]

for rec_data in sample_recommendations:
    recommendation, created = Recommendation.objects.get_or_create(
        user=alice,
        university_ref=rec_data['university_ref'],
        defaults=rec_data
    )
    
    if created:
        print(f"Created recommendation for Alice: {rec_data['university_ref']}")

# Create sample feedback
if sample_recommendations:
    first_rec = Recommendation.objects.filter(user=alice).first()
    if first_rec:
        feedback, created = Feedback.objects.get_or_create(
            user=alice,
            recommendation=first_rec,
            defaults={
                'rating': 5,
                'notes': 'Excellent recommendation! Stanford is exactly what I was looking for in terms of research opportunities and academic excellence.'
            }
        )
        
        if created:
            print(f"Created feedback for Alice's recommendation")

print("\nDemo data creation completed!")
print("\nDemo user credentials:")
print("- alice@example.com / demo123 (CS/AI student)")
print("- bob@example.com / demo123 (Engineering student)")  
print("- carol@example.com / demo123 (Medical student)")
print("\nAdmin panel: http://localhost:8000/admin/")
print("API docs: http://localhost:8000/api/docs/")
print("Health check: http://localhost:8000/api/healthz/")
