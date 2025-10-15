# LLM Prompts Examples for UniQuest

This document provides examples of how the comprehensive LLM prompts work in the UniQuest system.

## 1. University Scoring Prompt Example

### Input Data
```python
university_data = {
    'display_name': 'Stanford University',
    'country_code': 'US',
    'webometrics_rank': 2,
    'works_count': 125000,
    'cited_by_count': 2500000,
    'homepage_url': 'https://stanford.edu'
}

user_profile = {
    'gpa': 3.8,
    'gpa_scale': '4.0',
    'current_level': 'Undergraduate',
    'graduation_year': '2025',
    'test_scores_json': {'SAT': 1520, 'TOEFL': 110},
    'disciplines': ['Computer Science', 'Artificial Intelligence'],
    'career_goals': ['Software Engineering', 'AI Research'],
    'locations': ['United States', 'Canada'],
    'budget_min': 50000,
    'budget_max': 80000
}
```

### Generated Prompt
```
You are an expert university admissions counselor and academic advisor. Your task is to evaluate how well a specific university matches a student's profile and provide a compatibility score.

## STUDENT ACADEMIC PROFILE
**Academic Standing:**
- Current GPA: 3.8 (on 4.0 scale)
- Current Level: Undergraduate
- Expected Graduation: 2025

**Standardized Test Scores:**
- SAT: 1520
- TOEFL: 110

**Academic Interests & Goals:**
- Field of Study Interests: Computer Science, Artificial Intelligence
- Career Goals: Software Engineering, AI Research

**Geographic & Financial Preferences:**
- Preferred Locations: United States, Canada
- Budget Range: $50,000 - $80,000 per year

## UNIVERSITY PROFILE
**Institution Details:**
- Name: Stanford University
- Country: US
- Global Ranking: 2
- Research Output: 125,000 publications
- Citation Impact: 2,500,000 total citations
- Website: https://stanford.edu

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

Score:
```

### Expected LLM Response
```
0.82
```

## 2. Rationale Generation Prompt Example

### Input Data
```python
weights = {
    'academics': 0.4,
    'interests': 0.25,
    'career': 0.2,
    'location': 0.1,
    'budget': 0.03,
    'ranking': 0.01,
    'research_activity': 0.01
}
```

### Generated Prompt
```
You are an expert university admissions counselor providing personalized recommendations. Your task is to write a compelling, personalized rationale explaining why this specific university is an excellent match for this student.

## STUDENT PROFILE
**Academic Background:**
- GPA: 3.8 (on 4.0 scale)
- Current Level: Undergraduate
- Expected Graduation: 2025
- Test Scores: - SAT: 1520
- TOEFL: 110

**Academic Interests & Career Goals:**
- Field of Study: Computer Science, Artificial Intelligence
- Career Aspirations: Software Engineering, AI Research

**Preferences:**
- Preferred Locations: United States, Canada
- Budget Range: $50,000 - $80,000 per year

## UNIVERSITY PROFILE
**Institution:**
- Name: Stanford University
- Location: US
- Global Ranking: 2
- Research Output: 125,000 publications
- Citation Impact: 2,500,000 total citations

## RECOMMENDATION WEIGHTS
The student's priority factors (used in scoring):
- academics: 40.0%
- interests: 25.0%
- career: 20.0%
- location: 10.0%
- budget: 3.0%
- ranking: 1.0%
- research_activity: 1.0%

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

**Rationale:**
```

### Expected LLM Response
```
Stanford University is an excellent match for your strong academic profile (3.8 GPA, 1520 SAT) and aligns perfectly with your interests in Computer Science and AI. With your high priority on academics (40%) and career preparation (20%), Stanford's world-class CS program and Silicon Valley connections provide exceptional opportunities for your software engineering and AI research goals, though admission is competitive given the university's prestige.
```

## 3. Profile Analysis Prompt Example

### Generated Prompt
```
You are an expert university admissions counselor and academic advisor. Your task is to analyze this student's profile and provide comprehensive insights about their academic competitiveness, strengths, and recommendations for university applications.

## STUDENT ACADEMIC PROFILE
**Academic Standing:**
- Current GPA: 3.8 (on 4.0 scale)
- Current Level: Undergraduate
- Expected Graduation: 2025

**Standardized Test Scores:**
- SAT: 1520
- TOEFL: 110

**Academic Interests & Career Goals:**
- Field of Study Interests: Computer Science, Artificial Intelligence
- Career Aspirations: Software Engineering, AI Research

**Geographic & Financial Preferences:**
- Preferred Locations: United States, Canada
- Budget Range: $50,000 - $80,000 per year
- Language Requirements: No specific language requirements
- Visa Restrictions: No visa restrictions

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

**Analysis:**
```

### Expected LLM Response
```json
{
  "strengths": [
    "Strong academic performance with 3.8 GPA on 4.0 scale",
    "Excellent standardized test scores (SAT 1520, TOEFL 110)",
    "Clear academic focus in high-demand field (Computer Science/AI)",
    "Well-defined career goals in technology sector",
    "International perspective with strong English proficiency"
  ],
  "improvements": [
    "Consider adding leadership or research experience to strengthen profile",
    "Could benefit from more specific extracurricular activities in CS/AI"
  ],
  "university_tiers": {
    "reach": ["Stanford University", "MIT", "Carnegie Mellon University"],
    "target": ["UC Berkeley", "University of Washington", "Georgia Tech"],
    "safety": ["UC San Diego", "University of Texas Austin", "University of Illinois Urbana-Champaign"]
  },
  "recommendations": [
    "Apply to 8-10 universities across all tiers for optimal chances",
    "Consider applying to Canadian universities for cost savings",
    "Highlight any coding projects or AI-related experiences in applications",
    "Prepare strong essays connecting CS interests to career goals",
    "Apply early action/decision to top choice if available"
  ],
  "country_insights": [
    "US universities offer strongest CS programs but higher costs",
    "Canadian universities provide excellent value and easier immigration",
    "Consider both countries for diverse opportunities and backup options"
  ],
  "overall_assessment": "This student has a strong academic profile well-suited for competitive CS programs. With strategic application planning and focus on reach/target/safety balance, they should have excellent admission prospects to top-tier universities."
}
```

## Key Features of These Prompts

1. **Comprehensive Data Integration**: All prompts include student academic profile, university data from Kaggle, user preferences, and weights
2. **Admission Likelihood Context**: Each prompt considers realistic admission probabilities
3. **Weighted Prioritization**: Prompts adapt based on user's priority weights
4. **Structured Output**: Clear instructions for consistent LLM responses
5. **Professional Tone**: Maintains encouraging but realistic counseling approach
6. **Specific Examples**: Uses actual data from the system for realistic scenarios

## Integration Points

These prompts are designed to be called from:
- `LLMService.create_scoring_prompt()` - for university scoring
- `LLMService.create_rationale_prompt()` - for recommendation rationales  
- `LLMService.create_profile_analysis_prompt()` - for student profile analysis

The prompts are ready for integration with any LLM API that supports structured text generation.
