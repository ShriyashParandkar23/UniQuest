"""
LLM Service for UniQuest - Placeholder for External LLM API Integration

This service contains placeholders where external LLM API calls should be made.
All the complex LLM integration logic is replaced with simple API call TODOs.
"""

import logging
import json
from typing import Dict, Any, List, Optional
from django.core.cache import cache

logger = logging.getLogger(__name__)


class LLMService:
    """Service for integrating with external LLM APIs."""
    
    def __init__(self):
        pass
    
    def generate_rationale(
        self, 
        university_data: Dict[str, Any], 
        user_profile: Dict[str, Any], 
        weights: Dict[str, float]
    ) -> str:
        """
        Generate a personalized rationale for why a university is recommended.
        
        Args:
            university_data: University information from dataset
            user_profile: Student profile and preferences
            weights: Weights used in recommendation scoring
            
        Returns:
            Personalized rationale text
        """
        try:
            # Create cache key for this specific combination
            cache_key = f"rationale_{hash(str(university_data.get('id', '')))}_{hash(str(user_profile))}"
            
            # Check cache first
            cached_rationale = cache.get(cache_key)
            if cached_rationale:
                return cached_rationale
            
            # TODO (Vishal): Make API call to external LLM service
            # Example API call structure:
            # response = requests.post('https://your-llm-api.com/generate-rationale', json={
            #     'university_data': university_data,
            #     'user_profile': user_profile,
            #     'weights': weights,
            #     'prompt_type': 'university_rationale'
            # })
            # rationale = response.json()['rationale']
            
            # Fallback to simple rationale for now
            rationale = self._fallback_rationale(university_data, weights)
            
            # Cache the result for 1 hour
            cache.set(cache_key, rationale, 3600)
            
            return rationale
            
        except Exception as e:
            logger.error(f"Error generating rationale: {e}")
            # Fallback to simple rationale
            return self._fallback_rationale(university_data, weights)
    
    def create_rationale_prompt(self, university_data: Dict[str, Any], user_profile: Dict[str, Any], weights: Dict[str, float]) -> str:
        """
        Create comprehensive prompt for rationale generation.
        
        Args:
            university_data: University information from dataset
            user_profile: Student profile and preferences
            weights: Weights used in recommendation scoring
            
        Returns:
            Formatted prompt string for LLM
        """
        # Extract student academic profile
        gpa = user_profile.get('gpa', 'Not specified')
        gpa_scale = user_profile.get('gpa_scale', '4.0')
        current_level = user_profile.get('current_level', 'Not specified')
        graduation_year = user_profile.get('graduation_year', 'Not specified')
        test_scores = user_profile.get('test_scores_json', {})
        
        # Extract university data
        uni_name = university_data.get('display_name', 'Unknown University')
        uni_country = university_data.get('country_code', 'Unknown')
        uni_rank = university_data.get('webometrics_rank', 'Unranked')
        works_count = university_data.get('works_count', 0)
        cited_by_count = university_data.get('cited_by_count', 0)
        homepage_url = university_data.get('homepage_url', 'Not available')
        
        # Extract user preferences and weights
        filters = user_profile.get('filters', {})
        disciplines = user_profile.get('disciplines', [])
        career_goals = user_profile.get('career_goals', [])
        locations = user_profile.get('locations', [])
        budget_min = user_profile.get('budget_min', 0)
        budget_max = user_profile.get('budget_max', 0)
        
        # Format test scores
        test_scores_str = ""
        if test_scores:
            test_scores_str = "\n".join([f"- {test}: {score}" for test, score in test_scores.items()])
        else:
            test_scores_str = "No test scores provided"
        
        # Format disciplines and career goals
        disciplines_str = ", ".join(disciplines) if disciplines else "Not specified"
        career_goals_str = ", ".join(career_goals) if career_goals else "Not specified"
        locations_str = ", ".join(locations) if locations else "No specific location preference"
        
        # Format weights for context
        weights_str = "\n".join([f"- {factor}: {weight:.1%}" for factor, weight in weights.items()])
        
        prompt = f"""
You are an expert university admissions counselor providing personalized recommendations. Your task is to write a compelling, personalized rationale explaining why this specific university is an excellent match for this student.

## STUDENT PROFILE
**Academic Background:**
- GPA: {gpa} (on {gpa_scale} scale)
- Current Level: {current_level}
- Expected Graduation: {graduation_year}
- Test Scores: {test_scores_str}

**Academic Interests & Career Goals:**
- Field of Study: {disciplines_str}
- Career Aspirations: {career_goals_str}

**Preferences:**
- Preferred Locations: {locations_str}
- Budget Range: ${budget_min:,} - ${budget_max:,} per year

## UNIVERSITY PROFILE
**Institution:**
- Name: {uni_name}
- Location: {uni_country}
- Global Ranking: {uni_rank}
- Research Output: {works_count:,} publications
- Citation Impact: {cited_by_count:,} total citations

## RECOMMENDATION WEIGHTS
The student's priority factors (used in scoring):
{weights_str}

## ADMISSION LIKELIHOOD CONTEXT
Consider the student's competitiveness for admission:
- Academic profile strength relative to university standards
- Test scores vs. typical admitted student ranges
- Geographic diversity factors
- Program-specific admission competitiveness

## INSTRUCTIONS
Write a personalized, compelling rationale (2-3 sentences) that:

1. **Highlights the strongest match factors** based on the student's priorities (weights)
2. **Addresses admission likelihood** realistically but positively
3. **Connects student goals** to university strengths
4. **Uses specific details** from both profiles
5. **Maintains an encouraging, professional tone**

Focus on the most important factors based on the student's weights. If academics is weighted highly, emphasize academic fit. If career goals are important, highlight career preparation. If location matters, address geographic benefits.

**Tone:** Professional, encouraging, specific, and personalized.

**Length:** 2-3 sentences maximum.

**Rationale:**"""

        return prompt
    
    def score_university_match(
        self, 
        university_data: Dict[str, Any], 
        user_profile: Dict[str, Any]
    ) -> float:
        """
        Use external LLM API to score how well a university matches a student profile.
        
        Args:
            university_data: University information
            user_profile: Student profile and preferences
            
        Returns:
            Match score between 0.0 and 1.0
        """
        try:
            # TODO (Vishal): Make API call to external LLM service for scoring
            # Example API call structure:
            # response = requests.post('https://your-llm-api.com/score-match', json={
            #     'university_data': university_data,
            #     'user_profile': user_profile,
            #     'prompt_type': 'university_scoring'
            # })
            # score = float(response.json()['score'])
            # return max(0.0, min(1.0, score))
            
            # Fallback to simple scoring for now
            return self._fallback_score(university_data, user_profile)
            
        except Exception as e:
            logger.error(f"Error scoring university match: {e}")
            # Fallback to simple scoring
            return self._fallback_score(university_data, user_profile)
    
    def create_scoring_prompt(self, university_data: Dict[str, Any], user_profile: Dict[str, Any]) -> str:
        """
        Create comprehensive prompt for university scoring.
        
        Args:
            university_data: University information from dataset
            user_profile: Student profile and preferences
            
        Returns:
            Formatted prompt string for LLM
        """
        # Extract student academic profile
        gpa = user_profile.get('gpa', 'Not specified')
        gpa_scale = user_profile.get('gpa_scale', '4.0')
        current_level = user_profile.get('current_level', 'Not specified')
        graduation_year = user_profile.get('graduation_year', 'Not specified')
        test_scores = user_profile.get('test_scores_json', {})
        
        # Extract university data
        uni_name = university_data.get('display_name', 'Unknown University')
        uni_country = university_data.get('country_code', 'Unknown')
        uni_rank = university_data.get('webometrics_rank', 'Unranked')
        works_count = university_data.get('works_count', 0)
        cited_by_count = university_data.get('cited_by_count', 0)
        homepage_url = university_data.get('homepage_url', 'Not available')
        
        # Extract user preferences and weights
        filters = user_profile.get('filters', {})
        disciplines = user_profile.get('disciplines', [])
        career_goals = user_profile.get('career_goals', [])
        locations = user_profile.get('locations', [])
        budget_min = user_profile.get('budget_min', 0)
        budget_max = user_profile.get('budget_max', 0)
        
        # Format test scores
        test_scores_str = ""
        if test_scores:
            test_scores_str = "\n".join([f"- {test}: {score}" for test, score in test_scores.items()])
        else:
            test_scores_str = "No test scores provided"
        
        # Format disciplines and career goals
        disciplines_str = ", ".join(disciplines) if disciplines else "Not specified"
        career_goals_str = ", ".join(career_goals) if career_goals else "Not specified"
        locations_str = ", ".join(locations) if locations else "No specific location preference"
        
        prompt = f"""
You are an expert university admissions counselor and academic advisor. Your task is to evaluate how well a specific university matches a student's profile and provide a compatibility score.

## STUDENT ACADEMIC PROFILE
**Academic Standing:**
- Current GPA: {gpa} (on {gpa_scale} scale)
- Current Level: {current_level}
- Expected Graduation: {graduation_year}

**Standardized Test Scores:**
{test_scores_str}

**Academic Interests & Goals:**
- Field of Study Interests: {disciplines_str}
- Career Goals: {career_goals_str}

**Geographic & Financial Preferences:**
- Preferred Locations: {locations_str}
- Budget Range: ${budget_min:,} - ${budget_max:,} per year

## UNIVERSITY PROFILE
**Institution Details:**
- Name: {uni_name}
- Country: {uni_country}
- Global Ranking: {uni_rank}
- Research Output: {works_count:,} publications
- Citation Impact: {cited_by_count:,} total citations
- Website: {homepage_url}

## EVALUATION CRITERIA
Rate this university match on a scale of 0.0 to 1.0 based on:

1. **Academic Fit (30% weight)**: How well does the student's academic profile align with the university's standards and programs?
2. **Interest Alignment (20% weight)**: How well do the university's programs match the student's academic interests?
3. **Career Preparation (20% weight)**: How well does the university prepare students for their career goals?
4. **Location Suitability (10% weight)**: How well does the location match the student's preferences?
5. **Financial Feasibility (10% weight)**: How realistic is the financial fit?
6. **Prestige & Ranking (5% weight)**: How does the university's reputation align with student expectations?
7. **Research Opportunities (5% weight)**: How well does the university support research in the student's field?

## ADMISSION LIKELIHOOD ASSESSMENT
Consider the following factors for admission probability:
- Student's academic competitiveness relative to university standards
- Typical admission requirements for the university
- Student's test scores vs. university averages
- Geographic diversity considerations
- Program-specific admission rates

## INSTRUCTIONS
1. Analyze each criterion thoroughly
2. Consider admission likelihood realistically
3. Provide a single numerical score between 0.0 and 1.0
4. Respond with ONLY the score (e.g., "0.75") - no explanation needed

Score:"""

        return prompt
    
    def analyze_student_profile(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze student profile using external LLM API.
        
        Args:
            profile_data: Student profile information
            
        Returns:
            Analysis results with suggestions
        """
        try:
            # TODO (Vishal): Make API call to external LLM service for profile analysis
            # Example API call structure:
            # response = requests.post('https://your-llm-api.com/analyze-profile', json={
            #     'profile_data': profile_data,
            #     'prompt_type': 'profile_analysis'
            # })
            # analysis_result = response.json()
            # return analysis_result
            
            # Fallback for now
            return {
                'analysis': 'Profile analysis will be available once LLM API is integrated',
                'suggestions': ['Connect your LLM API for personalized suggestions'],
                'strengths': ['Add LLM integration to identify profile strengths']
            }
            
        except Exception as e:
            logger.error(f"Error analyzing profile: {e}")
            return {
                'analysis': 'Profile analysis unavailable',
                'suggestions': [],
                'strengths': []
            }
    
    def create_profile_analysis_prompt(self, profile_data: Dict[str, Any]) -> str:
        """
        Create comprehensive prompt for student profile analysis.
        
        Args:
            profile_data: Student profile information
            
        Returns:
            Formatted prompt string for LLM
        """
        # Extract student academic profile
        gpa = profile_data.get('gpa', 'Not specified')
        gpa_scale = profile_data.get('gpa_scale', '4.0')
        current_level = profile_data.get('current_level', 'Not specified')
        graduation_year = profile_data.get('graduation_year', 'Not specified')
        test_scores = profile_data.get('test_scores_json', {})
        
        # Extract preferences
        disciplines = profile_data.get('disciplines', [])
        career_goals = profile_data.get('career_goals', [])
        locations = profile_data.get('locations', [])
        budget_min = profile_data.get('budget_min', 0)
        budget_max = profile_data.get('budget_max', 0)
        language_requirements = profile_data.get('language_requirements', [])
        visa_restrictions = profile_data.get('visa_restrictions', [])
        
        # Format test scores
        test_scores_str = ""
        if test_scores:
            test_scores_str = "\n".join([f"- {test}: {score}" for test, score in test_scores.items()])
        else:
            test_scores_str = "No test scores provided"
        
        # Format lists
        disciplines_str = ", ".join(disciplines) if disciplines else "Not specified"
        career_goals_str = ", ".join(career_goals) if career_goals else "Not specified"
        locations_str = ", ".join(locations) if locations else "No specific location preference"
        language_req_str = ", ".join(language_requirements) if language_requirements else "No specific language requirements"
        visa_restrictions_str = ", ".join(visa_restrictions) if visa_restrictions else "No visa restrictions"
        
        prompt = f"""
You are an expert university admissions counselor and academic advisor. Your task is to analyze this student's profile and provide comprehensive insights about their academic competitiveness, strengths, and recommendations for university applications.

## STUDENT ACADEMIC PROFILE
**Academic Standing:**
- Current GPA: {gpa} (on {gpa_scale} scale)
- Current Level: {current_level}
- Expected Graduation: {graduation_year}

**Standardized Test Scores:**
{test_scores_str}

**Academic Interests & Career Goals:**
- Field of Study Interests: {disciplines_str}
- Career Aspirations: {career_goals_str}

**Geographic & Financial Preferences:**
- Preferred Locations: {locations_str}
- Budget Range: ${budget_min:,} - ${budget_max:,} per year
- Language Requirements: {language_req_str}
- Visa Restrictions: {visa_restrictions_str}

## ANALYSIS TASKS
Provide a comprehensive analysis in the following format:

### ACADEMIC STRENGTHS
List 3-5 key academic strengths and competitive advantages.

### AREAS FOR IMPROVEMENT
Identify 2-3 areas where the student could strengthen their profile.

### UNIVERSITY TIER RECOMMENDATIONS
Categorize universities into:
- **Reach Schools** (competitive but possible)
- **Target Schools** (good match for profile)
- **Safety Schools** (high admission probability)

### SPECIFIC RECOMMENDATIONS
Provide 3-5 actionable recommendations for:
- Academic preparation
- Application strategy
- Test score improvements (if applicable)
- Extracurricular activities
- Application timeline

### COUNTRY/REGION INSIGHTS
Based on preferences and profile, provide insights about:
- Best-fit countries/regions
- Admission competitiveness by region
- Cultural and academic considerations

## INSTRUCTIONS
1. Be specific and actionable in your recommendations
2. Consider the student's academic level and timeline
3. Address both strengths and areas for improvement
4. Provide realistic assessment of competitiveness
5. Consider financial and geographic constraints
6. Maintain an encouraging but honest tone

**Format your response as structured JSON with the following keys:**
- "strengths": [list of 3-5 strengths]
- "improvements": [list of 2-3 improvement areas]
- "university_tiers": {"reach": [list], "target": [list], "safety": [list]}
- "recommendations": [list of 3-5 actionable recommendations]
- "country_insights": [list of regional insights]
- "overall_assessment": "2-3 sentence summary"

**Analysis:**"""

        return prompt
    
    def _fallback_rationale(self, university_data: Dict[str, Any], weights: Dict[str, float]) -> str:
        """Generate simple rationale when LLM API is unavailable."""
        
        name = university_data.get('display_name', 'This university')
        reasons = []
        
        if university_data.get('webometrics_rank'):
            reasons.append(f"strong global ranking (#{university_data['webometrics_rank']})")
        
        if university_data.get('works_count', 0) > 10000:
            reasons.append("extensive research output")
        
        if university_data.get('country_code'):
            reasons.append(f"located in {university_data['country_code']}")
        
        if not reasons:
            reasons.append("matches your academic profile")
        
        return f"{name} is recommended for its {' and '.join(reasons[:2])}."
    
    def _fallback_score(self, university_data: Dict[str, Any], user_profile: Dict[str, Any]) -> float:
        """Simple scoring fallback when LLM API is unavailable."""
        
        score = 0.5  # Base score
        
        # Boost for ranking
        if university_data.get('webometrics_rank'):
            rank = university_data['webometrics_rank']
            if rank <= 100:
                score += 0.3
            elif rank <= 500:
                score += 0.2
            elif rank <= 1000:
                score += 0.1
        
        # Boost for research activity
        works = university_data.get('works_count', 0)
        if works > 50000:
            score += 0.1
        elif works > 10000:
            score += 0.05
        
        return min(1.0, score)