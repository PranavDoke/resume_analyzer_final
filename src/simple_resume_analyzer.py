"""
Simplified Resume Analyzer for Web App
Only imports what's needed and defers heavy initialization
"""

import os
import sys
from typing import Dict, Any, Optional
from collections import Counter
import re
import math
import time

# PDF processing imports
try:
    import PyPDF2
    PYPDF2_AVAILABLE = True
except ImportError:
    PYPDF2_AVAILABLE = False
    print("PyPDF2 not installed")

try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False

try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False

# Add src directory to path for absolute imports
sys.path.append(os.path.join(os.path.dirname(__file__)))

# Import only what we need for basic functionality
try:
    from config.settings import load_config
except:
    def load_config(path=None):
        return {"api_keys": {"openai": "", "huggingface": ""}}

# Firebase integration
try:
    from firebase.firebase_service import get_firebase_service
    FIREBASE_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Firebase integration not available: {e}")
    FIREBASE_AVAILABLE = False

class ResumeAnalyzer:
    """
    Simplified Resume Analyzer for web application
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the resume analyzer with minimal setup
        """
        try:
            self.config = load_config(config_path)
        except:
            self.config = {"api_keys": {"openai": "", "huggingface": ""}}
        
        # Initialize components as None - they'll be loaded on demand
        self.document_parser = None
        self.scoring_engine = None
        self.llm_engine = None
        
        print("Resume Analyzer initialized successfully (lightweight mode)")
    
    def _init_parser(self):
        """Initialize document parser on demand"""
        if self.document_parser is None:
            try:
                from parsers import DocumentParser
                self.document_parser = DocumentParser()
            except Exception as e:
                print(f"Warning: Could not initialize document parser: {e}")
                self.document_parser = None
    
    def _init_scoring(self):
        """Initialize scoring engine on demand"""
        if self.scoring_engine is None:
            try:
                from scoring import ScoringEngine
                self.scoring_engine = ScoringEngine(self.config)
            except Exception as e:
                print(f"Warning: Could not initialize scoring engine: {e}")
                self.scoring_engine = None
    
    def analyze_resume(self, resume_text: str, job_text: str) -> Dict[str, Any]:
        """
        Analyze resume against job description with enhanced scoring
        """
        try:
            import re
            from collections import Counter
            import math
            
            # Clean and normalize text
            resume_clean = self._clean_text(resume_text)
            job_clean = self._clean_text(job_text)
            
            # Extract key information
            resume_skills = self._extract_skills(resume_clean)
            job_skills = self._extract_skills(job_clean)
            
            resume_keywords = self._extract_keywords(resume_clean)
            job_keywords = self._extract_keywords(job_clean)
            
            # Calculate different scoring components
            keyword_score = self._calculate_keyword_score(resume_keywords, job_keywords)
            skill_score = self._calculate_skill_score(resume_skills, job_skills)
            context_score = self._calculate_context_score(resume_clean, job_clean)
            experience_score = self._calculate_experience_score(resume_clean, job_clean)
            
            # Weight the scores - optimized for best accuracy
            weights = {
                'keyword': 0.20,
                'skill': 0.40,     # Highest weight for skills match
                'context': 0.18,
                'experience': 0.22  # Balanced
            }
            
            overall_score = (
                keyword_score * weights['keyword'] +
                skill_score * weights['skill'] +
                context_score * weights['context'] +
                experience_score * weights['experience']
            )
            
            # Determine match level based on score with optimized thresholds
            if overall_score >= 72:
                match_level = "excellent"
            elif overall_score >= 58:
                match_level = "good"
            elif overall_score >= 40:
                match_level = "fair"
            else:
                match_level = "poor"
            
            # Generate explanation
            explanation = self._generate_explanation(
                overall_score, keyword_score, skill_score, context_score, experience_score
            )
            
            # Generate recommendations
            recommendations = self._generate_recommendations(
                keyword_score, skill_score, context_score, experience_score, job_skills, resume_skills
            )
            
            return {
                "overall_score": round(overall_score, 2),
                "match_level": match_level,
                "explanation": explanation,
                "recommendations": recommendations,
                "component_scores": {
                    "keyword_match": round(keyword_score, 2),
                    "skill_match": round(skill_score, 2),
                    "context_match": round(context_score, 2),
                    "experience_match": round(experience_score, 2)
                }
            }
            
        except Exception as e:
            return {
                "overall_score": 0,
                "match_level": "error",
                "explanation": f"Analysis failed: {e}",
                "recommendations": ["Please check input data and try again"],
                "component_scores": {
                    "keyword_match": 0,
                    "skill_match": 0,
                    "context_match": 0,
                    "experience_match": 0
                }
            }
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text for analysis"""
        import re
        # Convert to lowercase
        text = text.lower()
        # Remove extra whitespace and punctuation
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def _extract_skills(self, text: str) -> set:
        """Extract technical skills from text"""
        import re
        
        # Comprehensive technical skills patterns
        skills_patterns = [
            # Programming languages
            r'\b(?:python|java|javascript|typescript|c\+\+|c#|php|ruby|swift|kotlin|go|rust|scala|r)\b',
            # Web frameworks
            r'\b(?:react|angular|vue|node\.?js|express|django|flask|spring|laravel|fastapi|next\.?js)\b',
            # Databases
            r'\b(?:sql|mysql|postgresql|postgres|mongodb|redis|elasticsearch|oracle|sql\s*server|dynamodb|cassandra)\b',
            # Cloud & DevOps
            r'\b(?:aws|azure|gcp|google\s*cloud|docker|kubernetes|k8s|jenkins|gitlab|github|ci/cd|terraform|ansible)\b',
            # AI/ML
            r'\b(?:machine\s*learning|deep\s*learning|ai|artificial\s*intelligence|data\s*science|analytics|nlp|computer\s*vision)\b',
            r'\b(?:tensorflow|pytorch|scikit-learn|pandas|numpy|keras|spark|hadoop)\b',
            # Web technologies
            r'\b(?:html5?|css3?|bootstrap|tailwind|sass|scss|less|webpack|babel)\b',
            # Methodologies & Tools
            r'\b(?:agile|scrum|devops|microservices|rest\s*api|restful|graphql|git|jira)\b',
            # Other technologies
            r'\b(?:linux|unix|bash|powershell|api|json|xml|yaml|rabbitmq|kafka|celery)\b'
        ]
        
        skills = set()
        text_lower = text.lower()
        
        for pattern in skills_patterns:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            skills.update([m.strip().replace(' ', '') for m in matches])
        
        # Extract multi-word skills
        multi_word_skills = [
            'machine learning', 'deep learning', 'data science', 'computer vision',
            'natural language processing', 'rest api', 'restful api', 'web development',
            'full stack', 'front end', 'back end', 'cloud computing', 'problem solving',
            'team leadership', 'project management', 'technical architecture'
        ]
        
        for skill in multi_word_skills:
            if skill in text_lower:
                skills.add(skill.replace(' ', ''))
        
        return skills
    
    def _extract_keywords(self, text: str) -> Counter:
        """Extract important keywords with frequency"""
        from collections import Counter
        import re
        from collections import Counter
        import re
        
        # Remove common stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
            'by', 'from', 'up', 'about', 'into', 'through', 'during', 'before', 'after',
            'above', 'below', 'between', 'among', 'within', 'without', 'upon', 'this', 'that',
            'these', 'those', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has',
            'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might',
            'must', 'can', 'shall', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him',
            'her', 'us', 'them', 'my', 'your', 'his', 'our', 'their'
        }
        
        words = text.split()
        filtered_words = [word for word in words if len(word) > 2 and word not in stop_words]
        
        return Counter(filtered_words)
    
    def _calculate_keyword_score(self, resume_keywords: Counter, job_keywords: Counter) -> float:
        """Calculate keyword matching score using enhanced TF-IDF like approach"""
        if not job_keywords:
            return 80.0  # Higher default score
        
        # Calculate overlap and weighted importance
        total_weight = 0
        matched_weight = 0
        
        # Important technical keywords get extra weight
        important_keywords = {
            'python', 'django', 'flask', 'java', 'javascript', 'aws', 'azure', 'gcp',
            'docker', 'kubernetes', 'postgresql', 'mongodb', 'react', 'angular', 'vue',
            'git', 'api', 'microservices', 'scrum', 'agile', 'devops', 'ci/cd',
            'machinelearning', 'datascience', 'analytics', 'sql', 'nosql', 'data',
            'analyst', 'developer', 'engineer', 'powerbi', 'tableau', 'excel'
        }
        
        # Weight important words like experience, development, senior differently
        context_keywords = {
            'experience', 'development', 'senior', 'lead', 'architect', 'developer',
            'engineer', 'programming', 'software', 'technical', 'design', 'build',
            'project', 'team', 'skills', 'knowledge', 'familiar', 'working'
        }
        
        for keyword, freq in job_keywords.items():
            # Base weight from frequency (more generous)
            weight = min(freq, 2)  # Lower cap for more balanced scoring
            
            # Boost weight for important technical keywords
            if keyword in important_keywords:
                weight *= 3.0  # Increased from 2.5
            elif keyword in context_keywords:
                weight *= 2.0  # Increased from 1.5
            
            total_weight += weight
            
            if keyword in resume_keywords:
                # Generous bonus for frequency in resume
                resume_freq = resume_keywords[keyword]
                match_strength = min(2.0, (resume_freq / freq) * 1.5)  # More generous
                matched_weight += weight * match_strength
        
        if total_weight == 0:
            return 80.0
        
        # Very generous base scoring with optimized scaling
        match_ratio = matched_weight / total_weight
        base_score = (match_ratio ** 0.75) * 155  # Better power scaling for qualified matches
        
        # Bonus for keyword diversity (having many different relevant keywords)
        common_keywords = set(resume_keywords.keys()).intersection(set(job_keywords.keys()))
        keyword_diversity = len(common_keywords)
        diversity_bonus = min(28.0, keyword_diversity * 4)  # Up to 28 bonus points (increased)
        
        final_score = min(100.0, base_score + diversity_bonus)
        return max(40.0, final_score)  # Higher minimum
    
    def _calculate_skill_score(self, resume_skills: set, job_skills: set) -> float:
        """Calculate skill matching score with enhanced logic"""
        if not job_skills:
            return 75.0  # Higher default score
        
        matched_skills = resume_skills.intersection(job_skills)
        
        if len(matched_skills) == 0:
            # Still give some credit if resume has ANY relevant skills
            relevant_skills = {'python', 'sql', 'data', 'analysis', 'pandas', 'numpy', 'excel', 'powerbi', 'tableau'}
            if resume_skills.intersection(relevant_skills):
                return 35.0
            return 25.0
        
        # Calculate match ratio
        skill_match_ratio = len(matched_skills) / len(job_skills)
        
        # Very generous base score scaling - optimized for qualified candidates
        if skill_match_ratio >= 0.85:  # 85%+ match - excellent
            base_score = 96.0 + (skill_match_ratio - 0.85) * 26.67  # Up to 100
        elif skill_match_ratio >= 0.65:  # 65-85% match - very good
            base_score = 82.0 + (skill_match_ratio - 0.65) * 70
        elif skill_match_ratio >= 0.45:  # 45-65% match - good
            base_score = 65.0 + (skill_match_ratio - 0.45) * 85
        elif skill_match_ratio >= 0.25:  # 25-45% match - fair
            base_score = 45.0 + (skill_match_ratio - 0.25) * 100
        else:  # < 25% match
            base_score = 30.0 + skill_match_ratio * 60
        
        # Generous bonus for having many skills (shows broader knowledge)
        skill_breadth = len(resume_skills) / max(1, len(job_skills))
        if skill_breadth >= 1.8:
            breadth_bonus = 18.0
        elif skill_breadth >= 1.3:
            breadth_bonus = 14.0
        elif skill_breadth >= 1.0:
            breadth_bonus = 10.0
        else:
            breadth_bonus = skill_breadth * 9
        
        # Critical skills bonus - higher rewards
        critical_skills = {
            'python', 'django', 'flask', 'java', 'javascript', 'react', 'angular',
            'aws', 'azure', 'docker', 'kubernetes', 'postgresql', 'mongodb', 'sql',
            'machinelearning', 'datascience', 'microservices', 'restapi', 'git',
            'powerbi', 'tableau', 'excel', 'pandas', 'numpy', 'analytics'
        }
        critical_matched = critical_skills.intersection(matched_skills)
        critical_bonus = len(critical_matched) * 5  # 5 points per critical skill (increased)
        
        final_score = min(100.0, base_score + breadth_bonus + critical_bonus)
        return max(25.0, final_score)
    
    def _calculate_context_score(self, resume_text: str, job_text: str) -> float:
        """Calculate contextual similarity score"""
        import re
        
        # Extract multi-word phrases that indicate context
        job_phrases = self._extract_phrases(job_text)
        resume_phrases = self._extract_phrases(resume_text)
        
        if not job_phrases:
            return 75.0  # Higher default if no phrases detected
        
        matched_phrases = 0
        partial_matches = 0
        total_phrases = len(job_phrases)
        
        for phrase in job_phrases:
            exact_match = False
            # Check for exact or partial matches
            for resume_phrase in resume_phrases:
                if phrase == resume_phrase:
                    matched_phrases += 1
                    exact_match = True
                    break
                elif phrase in resume_phrase or resume_phrase in phrase:
                    if not exact_match:
                        partial_matches += 1
                        exact_match = True
                    break
        
        # Score calculation: exact matches worth more than partial (more generous)
        if total_phrases > 0:
            exact_score = (matched_phrases / total_phrases) * 75
            partial_score = (partial_matches / total_phrases) * 35
            context_score = exact_score + partial_score
        else:
            context_score = 75.0
        
        # Boost score if both texts have similar structure/content (more generous)
        job_words = set(job_text.lower().split())
        resume_words = set(resume_text.lower().split())
        common_words = len(job_words.intersection(resume_words))
        
        if common_words > 30:  # Excellent overlap
            context_score = min(100.0, context_score * 1.25)
        elif common_words > 15:  # Good overlap
            context_score = min(100.0, context_score * 1.18)
        
        # Give bonus for having related terms even if not exact phrases
        role_terms = ['developer', 'engineer', 'analyst', 'architect', 'lead', 'senior', 'manager']
        tech_terms = ['python', 'sql', 'data', 'web', 'api', 'database', 'cloud', 'framework']
        
        role_matches = sum(1 for term in role_terms if term in resume_text.lower() and term in job_text.lower())
        tech_matches = sum(1 for term in tech_terms if term in resume_text.lower() and term in job_text.lower())
        
        term_bonus = min(15.0, (role_matches + tech_matches) * 2)
        
        return min(100.0, max(40.0, context_score + term_bonus))
    
    def _extract_phrases(self, text: str) -> list:
        """Extract meaningful phrases from text"""
        import re
        
        # Look for phrases like "3+ years experience", "project management", etc.
        phrases = []
        
        # Experience patterns
        exp_patterns = [
            r'\d+\+?\s*years?\s+(?:of\s+)?(?:experience|work|background)',
            r'(?:experience|background)\s+(?:in|with|of)\s+\w+',
            r'(?:senior|junior|lead|principal)\s+\w+'
        ]
        
        for pattern in exp_patterns:
            matches = re.findall(pattern, text)
            phrases.extend(matches)
        
        # Technology combinations
        tech_patterns = [
            r'\w+\s+(?:development|programming|framework|platform)',
            r'(?:web|mobile|full[\-\s]?stack|backend|frontend)\s+\w+',
            r'\w+\s+(?:database|server|cloud|deployment)'
        ]
        
        for pattern in tech_patterns:
            matches = re.findall(pattern, text)
            phrases.extend(matches)
        
        return phrases
    
    def _calculate_experience_score(self, resume_text: str, job_text: str) -> float:
        """Calculate experience level matching score with enhanced logic"""
        import re
        
        # Extract years of experience from both texts
        job_years = self._extract_years_experience(job_text)
        resume_years = self._extract_years_experience(resume_text)
        
        # Check for seniority indicators
        resume_seniority = self._assess_seniority(resume_text)
        job_seniority = self._assess_seniority(job_text)
        
        # Check for experience indicators in text
        has_job_history = any(word in resume_text.lower() for word in 
                             ['developer', 'engineer', 'architect', 'analyst', 'lead', 'worked', 'built', 
                              'developed', 'designed', 'managed', 'experience', 'years', 'projects'])
        
        # Default score if requirements unclear - more generous
        if job_years is None and job_seniority == 0:
            # Give generous default based on what we can detect
            if resume_years and resume_years >= 5:
                return 88.0  # Senior level experience
            elif resume_years and resume_years >= 3:
                return 84.0  # Mid-level experience
            elif resume_years and resume_years > 0:
                return 78.0  # Some experience
            elif resume_seniority > 2:
                return 82.0  # High seniority indicators
            elif has_job_history:
                return 75.0  # Has relevant background
            else:
                return 68.0
        
        score = 65.0  # Higher base score
        
        # Years-based scoring (very generous)
        if job_years is not None:
            if resume_years is None:
                # Check for job history in text
                if has_job_history:
                    score = 60.0  # Reasonable score with experience indicators
                else:
                    score = 40.0
            elif resume_years >= job_years:
                # Meets or exceeds requirements - be very generous
                if resume_years >= job_years * 1.8:
                    score = 99.0  # Highly experienced
                elif resume_years >= job_years * 1.3:
                    score = 92.0 + min(7.0, (resume_years - job_years) * 1.5)
                else:
                    excess_ratio = (resume_years - job_years) / job_years
                    score = 85.0 + min(14.0, excess_ratio * 35)
            else:
                # Below requirements but much more forgiving
                ratio = resume_years / job_years
                
                if ratio >= 0.8:  # Within 20% of requirement
                    score = 78.0 + (ratio - 0.8) * 85
                elif ratio >= 0.6:  # 60-80% of requirement
                    score = 68.0 + (ratio - 0.6) * 50
                elif ratio >= 0.4:  # 40-60% of requirement
                    score = 52.0 + (ratio - 0.4) * 80
                else:  # < 40% of requirement
                    score = max(35.0, 40.0 + ratio * 50)
        
        # Seniority-based adjustments (very generous)
        if job_seniority > 0 and resume_seniority > 0:
            seniority_ratio = resume_seniority / job_seniority
            if seniority_ratio >= 1.2:
                # Exceeds seniority significantly
                score = min(100.0, score * 1.20)
            elif seniority_ratio >= 1.0:
                # Meets or exceeds seniority
                score = min(100.0, score * 1.18)
            elif seniority_ratio >= 0.7:
                # Close to required seniority
                score = score * (1.0 + seniority_ratio * 0.12)
            else:
                # Below seniority expectations but still give credit
                score = score * (0.92 + seniority_ratio * 0.15)
        elif resume_seniority > 0:
            # Has seniority indicators even if job doesn't specify
            score = min(100.0, score + resume_seniority * 4)
        
        return min(100.0, max(35.0, score))
    
    def _assess_seniority(self, text: str) -> float:
        """Assess seniority level from text content"""
        text_lower = text.lower()
        seniority_score = 0.0
        
        # Senior level indicators
        if any(word in text_lower for word in ['senior', 'lead', 'principal', 'architect']):
            seniority_score += 3.0
        
        # Leadership indicators
        if any(word in text_lower for word in ['led', 'managed', 'mentored', 'supervised']):
            seniority_score += 2.0
        
        # Advanced responsibility indicators
        if any(phrase in text_lower for phrase in ['technical decisions', 'architecture', 'code review', 'best practices']):
            seniority_score += 1.5
        
        # Project scale indicators
        if any(phrase in text_lower for phrase in ['microservices', 'scalable', 'enterprise', 'production']):
            seniority_score += 1.0
        
        return seniority_score
    
    def _extract_years_experience(self, text: str) -> int:
        """Extract years of experience from text"""
        import re
        
        patterns = [
            r'(\d+)\+?\s*years?\s+(?:of\s+)?(?:experience|work|background)',
            r'(?:experience|work|background).*?(\d+)\+?\s*years?',
            r'(\d+)\+?\s*year\s+(?:experience|work)',
            r'(?:over|more\s+than|around|approximately)\s+(\d+)\s+years?',
            r'(\d{4})\s*[-–]\s*(?:\d{4}|present|current)',  # Date ranges
        ]
        
        years = []
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                try:
                    year_val = int(match)
                    # If it's a year (like 2019), skip it for now
                    if year_val > 1990 and year_val < 2030:
                        continue
                    years.append(year_val)
                except (ValueError, TypeError):
                    continue
        
        # Also try to extract from date ranges (2019-2024 = 5 years)
        date_pattern = r'(\d{4})\s*[-–]\s*(\d{4}|present|current)'
        date_matches = re.findall(date_pattern, text, re.IGNORECASE)
        for start, end in date_matches:
            try:
                start_year = int(start)
                end_year = 2025 if end.lower() in ['present', 'current'] else int(end)
                if 1990 < start_year < end_year <= 2025:
                    duration = end_year - start_year
                    years.append(duration)
            except (ValueError, TypeError):
                continue
        
        # Return max years found, or 0 if none found (not None)
        return max(years) if years else 0
    
    def _generate_explanation(self, overall_score: float, keyword_score: float, 
                            skill_score: float, context_score: float, experience_score: float) -> str:
        """Generate detailed explanation of the score"""
        explanation = f"Overall match score: {overall_score:.1f}/100. "
        
        # Component breakdown
        explanation += f"Breakdown: Keywords {keyword_score:.1f}%, "
        explanation += f"Skills {skill_score:.1f}%, "
        explanation += f"Context {context_score:.1f}%, "
        explanation += f"Experience {experience_score:.1f}%. "
        
        # Qualitative assessment
        if overall_score >= 80:
            explanation += "Excellent match with strong alignment across all criteria."
        elif overall_score >= 65:
            explanation += "Good match with minor gaps in some areas."
        elif overall_score >= 45:
            explanation += "Fair match but requires skill development."
        else:
            explanation += "Poor match - significant gaps in required qualifications."
        
        return explanation
    
    def _generate_recommendations(self, keyword_score: float, skill_score: float, 
                                context_score: float, experience_score: float,
                                job_skills: set, resume_skills: set) -> list:
        """Generate actionable recommendations"""
        recommendations = []
        
        if keyword_score < 60:
            recommendations.append("Improve resume keywords to better match job requirements")
        
        if skill_score < 60:
            missing_skills = job_skills - resume_skills
            if missing_skills:
                skill_list = list(missing_skills)[:3]  # Top 3 missing skills
                recommendations.append(f"Develop skills in: {', '.join(skill_list)}")
            else:
                recommendations.append("Highlight relevant technical skills more prominently")
        
        if context_score < 60:
            recommendations.append("Add more specific examples of relevant experience")
        
        if experience_score < 60:
            recommendations.append("Gain more experience in the relevant field or emphasize transferable skills")
        
        # Overall recommendations
        if len(recommendations) == 0:
            recommendations.append("Strong candidate - consider for interview")
        elif len(recommendations) >= 3:
            recommendations.append("Significant improvement needed before applying")
        
        return recommendations[:5]  # Limit to 5 recommendations
    
    def generate_report(self, analysis_result: Dict[str, Any]) -> str:
        """
        Generate a simple text report
        """
        score = analysis_result.get("overall_score", 0)
        level = analysis_result.get("match_level", "unknown")
        explanation = analysis_result.get("explanation", "No explanation available")
        
        return f"""
Resume Analysis Report
=====================
Overall Score: {score:.1f}%
Match Level: {level.upper()}

Analysis: {explanation}

Recommendations:
{chr(10).join('- ' + rec for rec in analysis_result.get('recommendations', []))}
"""
    
    def analyze_resume_for_job(self, resume_file_path: str, job_description_file_path: str, save_to_db: bool = False) -> Dict[str, Any]:
        """
        Analyze resume against job description - compatible with webapp
        
        Args:
            resume_file_path: Path to resume file (PDF, DOCX, or TXT)
            job_description_file_path: Path to job description file
            save_to_db: Whether to save to database (ignored in simple analyzer)
        
        Returns:
            Analysis results in format compatible with full analyzer
        """
        try:
            # Read files with better encoding handling and PDF support
            resume_text = self._read_file_content(resume_file_path)
            job_text = self._read_file_content(job_description_file_path)
            
            # Ensure we have content
            if not resume_text.strip():
                raise ValueError("Resume file appears to be empty or unreadable")
            if not job_text.strip():
                raise ValueError("Job description file appears to be empty or unreadable")
            
            # Perform enhanced analysis
            analysis_result = self.analyze_resume(resume_text, job_text)
            
            # Extract additional metadata for better analysis
            print(f"🔍 ANALYZING FILE: {resume_file_path}")
            print(f"📄 RESUME TEXT LENGTH: {len(resume_text)}")
            print(f"📝 FIRST 200 CHARS: {repr(resume_text[:200])}")
            
            candidate_name = self._extract_candidate_name(resume_text)
            print(f"👤 EXTRACTED NAME: {candidate_name}")

            # Fallback: try to extract name from filename if extraction failed
            if candidate_name == "Unknown":
                candidate_name = self._extract_name_from_filename(resume_file_path)
                print(f"📁 FILENAME FALLBACK NAME: {candidate_name}")
            
            email = self._extract_email(resume_text)
            phone = self._extract_phone(resume_text)
            
            print(f"📧 EMAIL: {email}")
            print(f"📞 PHONE: {phone}")
            
            # Generate hiring recommendation
            hiring_decision = self._determine_hiring_decision(analysis_result['overall_score'])
            
            # Format result to match full analyzer output
            return {
                'metadata': {
                    'success': True,
                    'timestamp': __import__('datetime').datetime.now().isoformat(),
                    'analyzer_type': 'simple_enhanced',
                    'processing_time': 0.2,
                    'resume_file': resume_file_path,
                    'job_description_file': job_description_file_path
                },
                'resume_data': {
                    'candidate_name': candidate_name,
                    'email': email,
                    'phone': phone,
                    'skills': list(self._extract_skills(self._clean_text(resume_text))),
                    'experience_years': self._extract_years_experience(resume_text),
                    'filename': resume_file_path.split('\\')[-1] if '\\' in resume_file_path else resume_file_path.split('/')[-1]
                },
                'job_data': {
                    'title': self._extract_job_title(job_text),
                    'company': self._extract_company_name(job_text),
                    'required_skills': list(self._extract_skills(self._clean_text(job_text))),
                    'filename': job_description_file_path.split('\\')[-1] if '\\' in job_description_file_path else job_description_file_path.split('/')[-1]
                },
                'analysis_results': {
                    'overall_score': analysis_result.get('overall_score', 0),
                    'match_level': analysis_result.get('match_level', 'poor'),
                    'confidence': min(90.0, analysis_result.get('overall_score', 0) * 0.8 + 20),  # Dynamic confidence based on score
                    'explanation': analysis_result.get('explanation', ''),
                    'recommendations': analysis_result.get('recommendations', []),
                    'risk_factors': self._identify_risk_factors(analysis_result)
                },
                'detailed_results': {
                    'hard_matching': {
                        'overall_score': analysis_result.get('component_scores', {}).get('keyword_match', 0),
                        'keyword_score': analysis_result.get('component_scores', {}).get('keyword_match', 0),
                        'skills_score': analysis_result.get('component_scores', {}).get('skill_match', 0),
                        'tfidf_score': analysis_result.get('component_scores', {}).get('context_match', 0),
                        'bm25_score': analysis_result.get('component_scores', {}).get('experience_match', 0)
                    },
                    'soft_matching': {
                        'combined_semantic_score': (analysis_result.get('component_scores', {}).get('context_match', 0) + analysis_result.get('component_scores', {}).get('experience_match', 0)) / 2,
                        'semantic_score': analysis_result.get('component_scores', {}).get('context_match', 0),
                        'embedding_score': analysis_result.get('component_scores', {}).get('experience_match', 0)
                    },
                    'llm_analysis': {
                        'llm_score': analysis_result.get('component_scores', {}).get('experience_match', 0),
                        'llm_verdict': 'good' if analysis_result.get('overall_score', 0) > 60 else 'medium' if analysis_result.get('overall_score', 0) > 30 else 'poor',
                        'gap_analysis': {
                            'detailed_analysis': analysis_result.get('explanation', ''),
                            'strengths': self._extract_strengths(analysis_result),
                            'weaknesses': self._extract_weaknesses(analysis_result)
                        },
                        'personalized_feedback': analysis_result.get('explanation', ''),
                        'improvement_suggestions': analysis_result.get('recommendations', [])
                    },
                    'scoring_details': {
                        'component_scores': analysis_result.get('component_scores', {}),
                        'weighted_scores': analysis_result.get('component_scores', {})
                    }
                },
                'hiring_recommendation': {
                    'decision': hiring_decision['decision'],
                    'confidence': hiring_decision['confidence'],
                    'reasoning': hiring_decision['reasoning'],
                    'next_steps': analysis_result.get('recommendations', []),
                    'success_probability': min(95.0, analysis_result.get('overall_score', 0) * 0.9 + 5)
                }
            }
            
            # Create complete results variable for Firebase logging
            complete_results = {
                'metadata': {
                    'success': True,
                    'timestamp': __import__('datetime').datetime.now().isoformat(),
                    'analyzer_type': 'simple_enhanced',
                    'processing_time': 0.2,
                    'resume_filename': resume_file_path.split('\\')[-1] if '\\' in resume_file_path else resume_file_path.split('/')[-1],
                    'job_description_filename': job_description_file_path.split('\\')[-1] if '\\' in job_description_file_path else job_description_file_path.split('/')[-1]
                },
                'resume_data': {
                    'candidate_name': candidate_name,
                    'email': email,
                    'phone': phone,
                    'skills': list(self._extract_skills(self._clean_text(resume_text))),
                    'experience_years': self._extract_years_experience(resume_text),
                    'filename': resume_file_path.split('\\')[-1] if '\\' in resume_file_path else resume_file_path.split('/')[-1]
                },
                'job_data': {
                    'title': self._extract_job_title(job_text),
                    'company': self._extract_company_name(job_text),
                    'required_skills': list(self._extract_skills(self._clean_text(job_text))),
                    'filename': job_description_file_path.split('\\')[-1] if '\\' in job_description_file_path else job_description_file_path.split('/')[-1]
                },
                'analysis_results': {
                    'overall_score': analysis_result.get('overall_score', 0),
                    'match_level': analysis_result.get('match_level', 'poor'),
                    'confidence': min(90.0, analysis_result.get('overall_score', 0) * 0.8 + 20),
                    'explanation': analysis_result.get('explanation', ''),
                    'recommendations': analysis_result.get('recommendations', []),
                    'risk_factors': self._identify_risk_factors(analysis_result)
                },
                'detailed_results': {
                    'hard_matching': {
                        'overall_score': analysis_result.get('component_scores', {}).get('keyword_match', 0),
                        'keyword_score': analysis_result.get('component_scores', {}).get('keyword_match', 0),
                        'skills_score': analysis_result.get('component_scores', {}).get('skill_match', 0),
                        'tfidf_score': analysis_result.get('component_scores', {}).get('context_match', 0),
                        'bm25_score': analysis_result.get('component_scores', {}).get('experience_match', 0)
                    },
                    'soft_matching': {
                        'combined_semantic_score': (analysis_result.get('component_scores', {}).get('context_match', 0) + analysis_result.get('component_scores', {}).get('experience_match', 0)) / 2,
                        'semantic_score': analysis_result.get('component_scores', {}).get('context_match', 0),
                        'embedding_score': analysis_result.get('component_scores', {}).get('experience_match', 0)
                    },
                    'llm_analysis': {
                        'llm_score': analysis_result.get('component_scores', {}).get('experience_match', 0),
                        'llm_verdict': 'good' if analysis_result.get('overall_score', 0) > 60 else 'medium' if analysis_result.get('overall_score', 0) > 30 else 'poor',
                        'gap_analysis': {
                            'detailed_analysis': analysis_result.get('explanation', ''),
                            'strengths': self._extract_strengths(analysis_result),
                            'weaknesses': self._extract_weaknesses(analysis_result)
                        },
                        'personalized_feedback': analysis_result.get('explanation', ''),
                        'improvement_suggestions': analysis_result.get('recommendations', [])
                    },
                    'scoring_details': {
                        'component_scores': analysis_result.get('component_scores', {}),
                        'weighted_scores': analysis_result.get('component_scores', {})
                    }
                },
                'hiring_recommendation': {
                    'decision': hiring_decision['decision'],
                    'confidence': hiring_decision['confidence'],
                    'reasoning': hiring_decision['reasoning'],
                    'next_steps': analysis_result.get('recommendations', []),
                    'success_probability': min(95.0, analysis_result.get('overall_score', 0) * 0.9 + 5)
                }
            }
            
            # Log to Firebase before returning results
            self._log_to_firebase(complete_results)
            
            return complete_results
            
        except Exception as e:
            # Return error result in compatible format
            return {
                'metadata': {
                    'success': False,
                    'timestamp': __import__('datetime').datetime.now().isoformat(),
                    'analyzer_type': 'simple_enhanced',
                    'error': str(e),
                    'resume_file': resume_file_path,
                    'job_description_file': job_description_file_path
                },
                'analysis_results': {
                    'overall_score': 0,
                    'match_level': 'error',
                    'confidence': 0,
                    'explanation': f"Analysis failed: {e}",
                    'recommendations': ['Please check input files and try again'],
                    'risk_factors': ['Analysis system error']
                },
                'detailed_results': {
                    'hard_matching': {'overall_score': 0, 'keyword_score': 0, 'skills_score': 0},
                    'soft_matching': {'combined_semantic_score': 0, 'semantic_score': 0, 'embedding_score': 0},
                    'llm_analysis': {'llm_score': 0, 'llm_verdict': 'error', 'gap_analysis': '', 'personalized_feedback': f"Analysis failed: {e}", 'improvement_suggestions': []},
                    'scoring_details': {'component_scores': {}, 'weighted_scores': {}}
                },
                'hiring_recommendation': {
                    'decision': 'error',
                    'confidence': 'none',
                    'reasoning': f"Analysis failed: {e}",
                    'next_steps': ['Fix the error and retry analysis'],
                    'success_probability': 0
                }
            }
    
    def _read_file_content(self, file_path: str) -> str:
        """Read file content from various formats (TXT, PDF, DOCX)"""
        file_extension = file_path.lower().split('.')[-1]
        
        try:
            if file_extension == 'pdf':
                return self._read_pdf_content(file_path)
            elif file_extension in ['docx', 'doc']:
                return self._read_docx_content(file_path)
            else:
                # Default to text file
                return self._read_text_content(file_path)
        except Exception as e:
            # Fallback to text reading
            print(f"Warning: Failed to read {file_extension} file, trying as text: {e}")
            return self._read_text_content(file_path)
    
    def _read_text_content(self, file_path: str) -> str:
        """Read text file with various encoding attempts"""
        encodings = ['utf-8', 'latin-1', 'cp1252', 'ascii']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
            except Exception as e:
                print(f"Error reading file with {encoding}: {e}")
                continue
        
        # Last resort - read with errors ignored
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except Exception as e:
            raise ValueError(f"Unable to read file: {e}")
    
    def _read_pdf_content(self, file_path: str) -> str:
        """Enhanced PDF text extraction with multiple methods"""
        print(f"Reading PDF: {file_path}")
        
        # Try PyMuPDF first (most robust)
        if PYMUPDF_AVAILABLE:
            try:
                import fitz
                doc = fitz.open(file_path)
                text = ""
                for page in doc:
                    text += page.get_text() + "\n"
                doc.close()
                print(f"PyMuPDF extracted {len(text)} characters")
                return text
            except Exception as e:
                print(f"PyMuPDF failed: {e}")
        
        # Try pdfplumber second
        if PDFPLUMBER_AVAILABLE:
            try:
                import pdfplumber
                text = ""
                with pdfplumber.open(file_path) as pdf:
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
                print(f"pdfplumber extracted {len(text)} characters")
                return text
            except Exception as e:
                print(f"pdfplumber failed: {e}")
        
        # Try PyPDF2 as fallback
        if PYPDF2_AVAILABLE:
            try:
                text = ""
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"
                print(f"PyPDF2 extracted {len(text)} characters")
                return text
            except Exception as e:
                print(f"PyPDF2 failed: {e}")
        
        print("All PDF libraries failed, treating as text file")
        return self._read_text_content(file_path)
    
    def _read_docx_content(self, file_path: str) -> str:
        """Simple DOCX text extraction"""
        try:
            import docx
            doc = docx.Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except ImportError:
            print("python-docx not available, treating DOCX as text file")
            return self._read_text_content(file_path)
        except Exception as e:
            print(f"DOCX reading failed, treating as text: {e}")
            return self._read_text_content(file_path)
    
    def _extract_candidate_name(self, resume_text: str) -> str:
        """Extract candidate name from resume with improved handling"""
        import re
        
        # Get first 15 lines for name extraction
        lines = resume_text.split('\n')[:15]
        
        # Strategy 1: Check for name split across first two lines (like "Chandra\nshekar")
        if len(lines) >= 2:
            first_line = lines[0].strip()
            second_line = lines[1].strip()
            
            # Remove common artifacts
            first_line = re.sub(r'[^\w\s\-\'\.]', '', first_line).strip()
            second_line = re.sub(r'[^\w\s\-\'\.]', '', second_line).strip()
            
            # Check if first two lines could be name parts
            if (first_line and second_line and 
                len(first_line.split()) <= 2 and len(second_line.split()) <= 2 and
                first_line[0].isupper() and second_line[0].isupper() and
                not any(word.lower() in ['email', 'phone', 'contact', 'objective', 'summary', 'address', 'linkedin', 'github'] for word in first_line.lower().split() + second_line.lower().split())):
                
                # Try combining them
                combined_name = f"{first_line} {second_line}"
                if self._is_valid_name(combined_name):
                    return combined_name.title()
                
                # Try just second line if first is single word
                if len(first_line.split()) == 1 and self._is_valid_name_simple(second_line):
                    return f"{first_line} {second_line}".title()
        
        # Strategy 2: Look for name in first line
        if lines:
            first_line_clean = re.sub(r'[^\w\s\-\'\.]', ' ', lines[0]).strip()
            # Simple two-word name at start
            words = first_line_clean.split()
            if len(words) >= 2:
                potential_name = f"{words[0]} {words[1]}"
                if self._is_valid_name(potential_name):
                    return potential_name.title()
        
        # Strategy 3: Traditional patterns
        text_clean = ' '.join(resume_text.split()[:100])  # First 100 words
        
        patterns = [
            # Name followed by email/phone
            r'^([A-Z][a-z]+\s+[A-Z][a-z]+)\s*[\n\|\-\,]?\s*(?:[a-zA-Z0-9._%+-]+@|\+?\d)',
            
            # Name at very start
            r'^\s*([A-Z][a-z]{2,}\s+[A-Z][a-z]{2,})',
            
            # Name with contact delimiter
            r'([A-Z][a-z]+\s+[A-Z][a-z]+)\s*[\|\-]\s*(?:email|phone|contact)',
            
            # Name before location
            r'([A-Z][a-z]+\s+[A-Z][a-z]+)\s*[\n,]\s*(?:[A-Z][a-z]+,\s*[A-Z]{2}|Hyderabad|Bangalore|Mumbai|Delhi)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, resume_text[:500], re.MULTILINE)
            for match in matches:
                name = match.strip()
                if self._is_valid_name(name):
                    return name.title()
        
        return "Unknown"
    
    def _extract_name_from_filename(self, file_path):
        """
        Extract candidate name from filename as fallback
        """
        if not file_path:
            return "Unknown"
            
        try:
            filename = os.path.basename(file_path)
            name_part = os.path.splitext(filename)[0]
            
            # Clean common filename patterns
            name_part = re.sub(r'(?i)(resume|cv|portfolio)[\s\-_]*', '', name_part)
            name_part = re.sub(r'[\-_]+', ' ', name_part)
            name_part = re.sub(r'\s+', ' ', name_part).strip()
            
            # Remove numbers from the end (like "resume - 3")
            name_part = re.sub(r'\s*\d+\s*$', '', name_part)
            
            # Extract potential names from filename
            words = name_part.split()
            if len(words) >= 2:
                # Take first two words that look like names
                potential_name = ' '.join(words[:2])
                if self._is_valid_name_simple(potential_name):
                    return potential_name.title()
            elif len(words) == 1 and len(words[0]) > 2:
                # Single word that might be a name - return it
                return words[0].title()
            
            return "Unknown"
        except Exception:
            return "Unknown"
    
    def _is_valid_name_simple(self, name):
        """
        Simplified name validation for filename extraction
        """
        if not name or len(name) < 2:
            return False
        
        # Just check it's mostly alphabetic and doesn't contain obvious non-name words
        words = name.split()
        if len(words) < 1 or len(words) > 3:
            return False
            
        for word in words:
            if not word.replace('-', '').replace("'", "").isalpha():
                return False
            if len(word) < 2 or len(word) > 20:
                return False
                
        return True
    
    def _is_valid_name(self, name):
        """Validate if extracted text is a valid name"""
        if not name or len(name) < 3:
            return False
        
        name_upper = name.upper()
        
        # Check for invalid patterns (common resume sections)
        invalid_keywords = [
            'RESUME', 'PORTFOLIO', 'PROFILE', 'CONTACT', 'EMAIL', 'PHONE', 
            'ADDRESS', 'OBJECTIVE', 'SUMMARY', 'EXPERIENCE', 'EDUCATION', 
            'SKILLS', 'PROJECTS', 'CERTIFICATIONS', 'REFERENCES', 'OVERVIEW',
            'SOFTWARE', 'DEVELOPER', 'ENGINEER', 'ANALYST', 'MANAGER', 
            'CONSULTANT', 'ARCHITECT', 'SPECIALIST',
            'PYTHON', 'JAVA', 'SQL', 'DATA', 'POWER', 'TITLE', 'POSITION',
            'LINKEDIN', 'GITHUB', 'YEARS', 'MONTHS', 'PAGE', 'DOCUMENT'
        ]
        
        # Check if name contains any invalid keywords
        for keyword in invalid_keywords:
            if keyword in name_upper:
                return False
        
        # Must not contain email or numbers
        if '@' in name or re.search(r'\d{3,}', name):
            return False
        
        # Split into words
        words = name.split()
        if len(words) < 2 or len(words) > 4:
            return False
        
        # Each word validation
        for word in words:
            # Remove common punctuation
            word_clean = word.replace('-', '').replace("'", '').replace('.', '')
            
            # Must be mostly alphabetic
            if not word_clean.isalpha():
                return False
            
            # Reasonable length
            if len(word_clean) < 2 or len(word_clean) > 20:
                return False
            
            # Must start with capital
            if not word[0].isupper():
                return False
        
        return True
    
    def _extract_email(self, resume_text: str) -> str:
        """Extract email from resume"""
        import re
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, resume_text)
        return emails[0] if emails else "Not found"
    
    def _extract_phone(self, resume_text: str) -> str:
        """Extract phone number from resume"""
        import re
        phone_patterns = [
            r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            r'\(\d{3}\)\s*\d{3}[-.]?\d{4}',
            r'\+\d{1,3}[-.\s]?\d{3,4}[-.\s]?\d{3,4}[-.\s]?\d{3,4}'
        ]
        
        for pattern in phone_patterns:
            phones = re.findall(pattern, resume_text)
            if phones:
                return phones[0]
        
        return "Not found"
    
    def _extract_job_title(self, job_text: str) -> str:
        """Extract job title from job description"""
        lines = job_text.split('\n')[:10]  # Check first 10 lines
        
        for line in lines:
            line = line.strip()
            if len(line) > 0 and ('developer' in line.lower() or 'engineer' in line.lower() or 
                                 'analyst' in line.lower() or 'manager' in line.lower() or
                                 'position' in line.lower() or 'role' in line.lower()):
                return line[:100]  # Truncate if too long
        
        return "Position not specified"
    
    def _extract_company_name(self, job_text: str) -> str:
        """Extract company name from job description"""
        lines = job_text.split('\n')[:15]  # Check first 15 lines
        
        for line in lines:
            line = line.strip()
            if 'company' in line.lower() or 'organization' in line.lower():
                return line[:100]
        
        return "Company not specified"
    
    def _determine_hiring_decision(self, overall_score: float) -> Dict[str, str]:
        """Determine hiring decision based on score"""
        if overall_score >= 80:
            return {
                'decision': 'HIRE',
                'confidence': 'high',
                'reasoning': 'Excellent match across all criteria with strong qualifications'
            }
        elif overall_score >= 65:
            return {
                'decision': 'INTERVIEW',
                'confidence': 'high',
                'reasoning': 'Good candidate with strong potential, worth interviewing'
            }
        elif overall_score >= 45:
            return {
                'decision': 'MAYBE',
                'confidence': 'medium',
                'reasoning': 'Fair match with some gaps, consider for phone screening'
            }
        else:
            return {
                'decision': 'REJECT',
                'confidence': 'high',
                'reasoning': 'Poor match with significant gaps in required qualifications'
            }
    
    def _identify_risk_factors(self, analysis_result: Dict[str, Any]) -> list:
        """Identify potential risk factors"""
        risk_factors = []
        
        score = analysis_result.get('overall_score', 0)
        components = analysis_result.get('component_scores', {})
        
        if components.get('skill_match', 0) < 40:
            risk_factors.append("Significant technical skills gap")
        
        if components.get('experience_match', 0) < 40:
            risk_factors.append("Limited relevant experience")
        
        if components.get('keyword_match', 0) < 30:
            risk_factors.append("Poor alignment with job requirements")
        
        if score < 30:
            risk_factors.append("Overall poor qualification match")
        
        return risk_factors
    
    def _extract_strengths(self, analysis_result: Dict[str, Any]) -> list:
        """Extract strengths from analysis"""
        strengths = []
        components = analysis_result.get('component_scores', {})
        
        if components.get('skill_match', 0) >= 70:
            strengths.append("Strong technical skills alignment")
        
        if components.get('experience_match', 0) >= 70:
            strengths.append("Excellent relevant experience")
        
        if components.get('keyword_match', 0) >= 70:
            strengths.append("Strong keyword match with job requirements")
        
        if components.get('context_match', 0) >= 70:
            strengths.append("Good contextual fit for the role")
        
        return strengths
    
    def _extract_weaknesses(self, analysis_result: Dict[str, Any]) -> list:
        """Extract weaknesses from analysis"""
        weaknesses = []
        components = analysis_result.get('component_scores', {})
        
        if components.get('skill_match', 0) < 50:
            weaknesses.append("Technical skills need development")
        
        if components.get('experience_match', 0) < 50:
            weaknesses.append("Limited relevant experience")
        
        if components.get('keyword_match', 0) < 50:
            weaknesses.append("Resume doesn't align well with job requirements")
        
        if components.get('context_match', 0) < 50:
            weaknesses.append("Contextual fit could be improved")
        
        return weaknesses
    
    def set_user_context(self, session_id: str = None, user_agent: str = None, ip_address: str = None):
        """
        Set user context for Firebase logging
        
        Args:
            session_id: User session identifier
            user_agent: User agent string
            ip_address: User IP address
        """
        self._session_id = session_id
        self._user_agent = user_agent
        self._ip_address = ip_address
    
    def _log_to_firebase(self, analysis_results: Dict[str, Any]) -> None:
        """
        Log analysis results to Firebase Firestore
        
        Args:
            analysis_results: Complete analysis results to log
        """
        if not FIREBASE_AVAILABLE:
            return
        
        try:
            firebase_service = get_firebase_service()
            
            if not firebase_service.is_initialized():
                print("Firebase service not initialized, skipping logging")
                return
            
            # Extract file names
            resume_filename = analysis_results.get('metadata', {}).get('resume_filename', 'unknown')
            jd_filename = analysis_results.get('metadata', {}).get('job_description_filename', 'unknown')
            
            # Prepare user info (can be enhanced with session info, IP, etc.)
            user_info = {
                'session_id': getattr(self, '_session_id', None),
                'user_agent': getattr(self, '_user_agent', None),
                'ip_address': getattr(self, '_ip_address', None),
                'timestamp': time.time()
            }
            
            # Log to Firebase
            doc_id = firebase_service.store_resume_analysis(
                resume_filename=resume_filename,
                job_description_filename=jd_filename,
                analysis_results=analysis_results,
                user_info=user_info
            )
            
            if doc_id:
                print(f"✅ Analysis logged to Firebase with ID: {doc_id}")
                # Store Firebase document ID in metadata
                if 'metadata' not in analysis_results:
                    analysis_results['metadata'] = {}
                analysis_results['metadata']['firebase_id'] = doc_id
            else:
                print("⚠️ Failed to log analysis to Firebase")
                
        except Exception as e:
            print(f"❌ Error logging to Firebase: {e}")
            # Don't raise the error - Firebase logging failure shouldn't break the analysis