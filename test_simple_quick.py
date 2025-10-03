"""
Quick test to verify simple analyzer produces different results
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.simple_resume_analyzer import ResumeAnalyzer

def test_simple_analyzer():
    """Test simple analyzer with different content"""
    
    analyzer = ResumeAnalyzer()
    
    # Very different resumes
    python_dev = """
    John Smith - Senior Python Developer
    5+ years Python, Django, Flask, AWS, Machine Learning, TensorFlow
    Built scalable web apps, REST APIs, led development teams
    Strong programming and software architecture experience
    """
    
    business_analyst = """  
    Mary Johnson - Business Analyst
    Excel, PowerBI, SQL, Business Intelligence, Financial Analysis
    No programming experience, focus on business reporting
    Created dashboards, analyzed sales data, presented to executives
    """
    
    python_job = """
    Senior Python Developer - 5+ years required
    Python, Django, Flask, REST APIs, AWS, Machine Learning
    Lead development projects, mentor team, software architecture
    """
    
    print("Testing Simple Analyzer...")
    
    # Test Python developer vs Python job
    result1 = analyzer.analyze_resume(python_dev, python_job)
    print(f"Python Dev vs Python Job: {result1['overall_score']:.1f} ({result1['match_level']})")
    print(f"  - Skills: {result1['component_scores']['skill_match']:.1f}")
    print(f"  - Keywords: {result1['component_scores']['keyword_match']:.1f}")
    
    # Test Business analyst vs Python job  
    result2 = analyzer.analyze_resume(business_analyst, python_job)
    print(f"Business Analyst vs Python Job: {result2['overall_score']:.1f} ({result2['match_level']})")
    print(f"  - Skills: {result2['component_scores']['skill_match']:.1f}")
    print(f"  - Keywords: {result2['component_scores']['keyword_match']:.1f}")
    
    difference = abs(result1['overall_score'] - result2['overall_score'])
    print(f"\nScore Difference: {difference:.1f} points")
    
    if difference > 20:
        print("✅ SUCCESS: Analyzer correctly differentiates between candidates!")
        return True
    else:
        print("❌ ISSUE: Scores too similar")
        return False

if __name__ == "__main__":
    test_simple_analyzer()