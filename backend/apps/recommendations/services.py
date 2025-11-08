import logging
from typing import List, Dict, Any
from django.contrib.auth import get_user_model
from .models import Recommendation
from ..dataset.services import DatasetService
from ..preferences.models import Preference
from ..llm.services import LLMService

User = get_user_model()
logger = logging.getLogger(__name__)


class RecommendationService:
    """Service for generating university recommendations with LLM integration."""
    
    def __init__(self):
        self.dataset_service = DatasetService()
        self.llm_service = LLMService()
    
    def generate_recommendations(
        self, 
        user: User, 
        filters: Dict[str, Any], 
        weights: Dict[str, float], 
        top_n: int = 20
    ) -> List[Recommendation]:
        """
        Generate recommendations for a user using LLM for rationale generation.
        
        Args:
            user: User to generate recommendations for
            filters: Filters to apply to university search
            weights: Weights for different recommendation factors
            top_n: Number of top recommendations to return
            
        Returns:
            List of Recommendation objects
        """
        try:
            # Get user preferences if weights not provided
            if not weights:
                try:
                    preference = Preference.objects.get(user=user)
                    weights = preference.weights
                except Preference.DoesNotExist:
                    weights = Preference().get_default_weights()
            
            # Get user profile for LLM context
            user_profile = self._build_user_profile(user, filters)
            
            # Get basic university matches from dataset (without complex scoring)
            dataset_recommendations = self.dataset_service.get_matching_universities(
                filters=filters,
                limit=top_n * 2  # Get more candidates for LLM scoring
            )
            
            # Use LLM to score and rank universities
            scored_recommendations = []
            for rec_data in dataset_recommendations:
                # Use LLM for scoring
                llm_score = self.llm_service.score_university_match(rec_data, user_profile)
                
                # Apply user weights to adjust score
                final_score = self._apply_user_weights(llm_score, weights)
                
                rec_data['score'] = final_score
                scored_recommendations.append(rec_data)
            
            # Sort by score and take top N
            scored_recommendations.sort(key=lambda x: x['score'], reverse=True)
            top_recommendations = scored_recommendations[:top_n]
            
            # Delete existing recommendations for this user to avoid clutter
            Recommendation.objects.filter(user=user).delete()
            
            # Create Recommendation objects with LLM-generated rationales
            recommendations = []
            for i, rec_data in enumerate(top_recommendations):
                # Generate personalized rationale using LLM
                rationale = self.llm_service.generate_rationale(
                    university_data=rec_data,
                    user_profile=user_profile,
                    weights=weights
                )
                
                recommendation = Recommendation.objects.create(
                    user=user,
                    university_ref=rec_data['id'],
                    program=rec_data.get('suggested_program'),
                    score=rec_data['score'],
                    rationale=rationale,
                    filters=filters,
                    weights=weights
                )
                recommendations.append(recommendation)
            
            logger.info(f"Generated {len(recommendations)} LLM-powered recommendations for user {user.id}")
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating recommendations for user {user.id}: {str(e)}")
            raise
    
    def _build_user_profile(self, user: User, filters: Dict[str, Any]) -> Dict[str, Any]:
        """Build comprehensive user profile for LLM context."""
        
        profile = {
            'user_id': user.id,
            'email': user.email,
            'filters': filters
        }
        
        # Add student profile data if available
        try:
            from ..students.models import StudentProfile
            student_profile = StudentProfile.objects.get(user=user)
            profile.update({
                'gpa': student_profile.gpa,
                'gpa_scale': student_profile.gpa_scale,
                'current_level': student_profile.current_level,
                'graduation_year': student_profile.graduation_year,
                'test_scores_json': student_profile.test_scores_json
            })
        except:
            pass
        
        # Add preferences if available
        try:
            preference = Preference.objects.get(user=user)
            profile.update({
                'disciplines': preference.disciplines,
                'career_goals': preference.career_goals,
                'locations': preference.locations,
                'budget_min': preference.budget_min,
                'budget_max': preference.budget_max,
                'language_requirements': preference.language_requirements,
                'visa_restrictions': preference.visa_restrictions
            })
        except:
            pass
        
        return profile
    
    def _apply_user_weights(self, base_score: float, weights: Dict[str, float]) -> float:
        """Apply user preference weights to adjust LLM base score."""
        
        # This is a simple adjustment - in practice you might want more sophisticated weighting
        weight_factor = sum(weights.values()) / len(weights) if weights else 1.0
        
        # Adjust score based on overall preference intensity
        adjusted_score = base_score * weight_factor
        
        return max(0.0, min(1.0, adjusted_score))  # Clamp between 0 and 1