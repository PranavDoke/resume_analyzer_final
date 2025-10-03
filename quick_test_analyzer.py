import sys, os
sys.path.insert(0, '.')
from src.simple_resume_analyzer import ResumeAnalyzer

analyzer = ResumeAnalyzer()

# Test with very different text
resume1 = 'John Python Developer Django Flask 5 years experience machine learning AWS'
resume2 = 'Sarah Excel PowerBI analyst business data visualization no programming'
job = 'Python Developer Django Flask required 3+ years machine learning'

print('Resume 1 (Python Expert):')
result1 = analyzer.analyze_resume(resume1, job)
print(f'Score: {result1["overall_score"]}, Skills: {result1["component_scores"]["skill_match"]}')

print('\nResume 2 (Excel Analyst):')
result2 = analyzer.analyze_resume(resume2, job)
print(f'Score: {result2["overall_score"]}, Skills: {result2["component_scores"]["skill_match"]}')

print(f'\nDifference in scores: {abs(result1["overall_score"] - result2["overall_score"])}')