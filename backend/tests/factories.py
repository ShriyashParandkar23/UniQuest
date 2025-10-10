"""
Test factories for UniQuest models using Factory Boy.

These factories create test data for use in unit and integration tests.
"""

import factory
from factory.django import DjangoModelFactory
from factory import fuzzy
from django.contrib.auth import get_user_model
from apps.students.models import StudentProfile
from apps.preferences.models import Preference
from apps.recommendations.models import Recommendation
from apps.feedback.models import Feedback
from apps.dataset.models import IngestionRun

User = get_user_model()


class UserFactory(DjangoModelFactory):
    """Factory for User model."""
    
    class Meta:
        model = User
    
    email = factory.Sequence(lambda n: f"user{n}@example.com")
    username = factory.Sequence(lambda n: f"user{n}")
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    is_verified = True
    
    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        if not create:
            return
        
        password = extracted or 'testpass123'
        self.set_password(password)
        self.save()


class StudentProfileFactory(DjangoModelFactory):
    """Factory for StudentProfile model."""
    
    class Meta:
        model = StudentProfile
    
    user = factory.SubFactory(UserFactory)
    gpa = fuzzy.FuzzyDecimal(2.0, 4.0, precision=2)
    interests = factory.Faker('text', max_nb_chars=200)
    goals = factory.Faker('text', max_nb_chars=300)
    country_preference = fuzzy.FuzzyChoice(['US', 'CA', 'GB', 'AU', 'DE'])
    budget_min = fuzzy.FuzzyInteger(10000, 30000)
    budget_max = fuzzy.FuzzyInteger(40000, 100000)
    
    test_scores = factory.LazyFunction(lambda: {
        'GRE': fuzzy.FuzzyInteger(280, 340).fuzz(),
        'TOEFL': fuzzy.FuzzyInteger(80, 120).fuzz(),
    })
    
    preferred_regions = factory.LazyFunction(lambda: [
        fuzzy.FuzzyChoice(['North America', 'Europe', 'Asia', 'Oceania']).fuzz()
    ])


class PreferenceFactory(DjangoModelFactory):
    """Factory for Preference model."""
    
    class Meta:
        model = Preference
    
    user = factory.SubFactory(UserFactory)
    
    weights = factory.LazyFunction(lambda: {
        'academics': 0.3,
        'interests': 0.2,
        'career': 0.2,
        'location': 0.1,
        'budget': 0.1,
        'ranking': 0.05,
        'research_activity': 0.05
    })


class RecommendationFactory(DjangoModelFactory):
    """Factory for Recommendation model."""
    
    class Meta:
        model = Recommendation
    
    user = factory.SubFactory(UserFactory)
    university_ref = factory.Sequence(lambda n: f"https://openalex.org/I{n:08d}")
    program = fuzzy.FuzzyChoice([
        'Computer Science', 'Engineering', 'Business',
        'Medicine', 'Law', 'Arts', None
    ])
    score = fuzzy.FuzzyFloat(0.1, 1.0)
    rationale = factory.Faker('text', max_nb_chars=500)
    
    filters = factory.LazyFunction(lambda: {
        'country': fuzzy.FuzzyChoice(['US', 'CA', 'GB']).fuzz()
    })
    
    weights = factory.LazyFunction(lambda: {
        'academics': 0.4,
        'research_activity': 0.3,
        'ranking': 0.2,
        'location': 0.1
    })


class FeedbackFactory(DjangoModelFactory):
    """Factory for Feedback model."""
    
    class Meta:
        model = Feedback
    
    user = factory.SubFactory(UserFactory)
    recommendation = factory.SubFactory(RecommendationFactory)
    rating = fuzzy.FuzzyInteger(1, 5)
    notes = factory.Faker('text', max_nb_chars=300)


class IngestionRunFactory(DjangoModelFactory):
    """Factory for IngestionRun model."""
    
    class Meta:
        model = IngestionRun
    
    source = fuzzy.FuzzyChoice(['openalex', 'webometrics', 'curation'])
    version = factory.Sequence(lambda n: f"2025.{n:02d}")
    status = fuzzy.FuzzyChoice(['SUCCESS', 'FAILED', 'RUNNING', 'PENDING'])
    
    stats = factory.LazyFunction(lambda: {
        'total_institutions': fuzzy.FuzzyInteger(1000, 50000).fuzz(),
        'processed_count': fuzzy.FuzzyInteger(900, 45000).fuzz(),
    })
    
    error = factory.Maybe(
        'status',
        yes_declaration='',
        no_declaration=factory.Faker('sentence'),
        condition=lambda obj: obj.status != 'FAILED'
    )


# Trait factories for specific scenarios
class CompletedStudentFactory(StudentProfileFactory):
    """Factory for a student with complete profile."""
    
    gpa = 3.5
    interests = "Computer Science, Machine Learning, Artificial Intelligence"
    goals = "Pursue PhD in AI and contribute to cutting-edge research"
    country_preference = "US"
    budget_min = 20000
    budget_max = 80000
    
    test_scores = {
        'GRE': 325,
        'TOEFL': 105,
        'SAT': 1450
    }
    
    preferred_regions = ["North America", "Europe"]


class HighPerformingStudentFactory(StudentProfileFactory):
    """Factory for high-performing student."""
    
    gpa = fuzzy.FuzzyDecimal(3.7, 4.0, precision=2)
    
    test_scores = factory.LazyFunction(lambda: {
        'GRE': fuzzy.FuzzyInteger(320, 340).fuzz(),
        'TOEFL': fuzzy.FuzzyInteger(100, 120).fuzz(),
    })


class BudgetConstrainedStudentFactory(StudentProfileFactory):
    """Factory for budget-constrained student."""
    
    budget_min = fuzzy.FuzzyInteger(5000, 15000)
    budget_max = fuzzy.FuzzyInteger(15000, 30000)


class InternationalStudentFactory(StudentProfileFactory):
    """Factory for international student."""
    
    country_preference = fuzzy.FuzzyChoice(['US', 'CA', 'GB', 'AU'])
    
    test_scores = factory.LazyFunction(lambda: {
        'TOEFL': fuzzy.FuzzyInteger(90, 120).fuzz(),
        'IELTS': fuzzy.FuzzyFloat(6.5, 9.0).fuzz(),
    })


class SuccessfulIngestionRunFactory(IngestionRunFactory):
    """Factory for successful ingestion run."""
    
    status = 'SUCCESS'
    error = ''
    finished_at = factory.Faker('date_time_this_month')


class FailedIngestionRunFactory(IngestionRunFactory):
    """Factory for failed ingestion run."""
    
    status = 'FAILED'
    error = factory.Faker('sentence')
    finished_at = factory.Faker('date_time_this_month')
