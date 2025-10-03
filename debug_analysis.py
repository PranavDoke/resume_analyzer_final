"""
Test script to debug why the analyzer produces the same results for different resumes
"""

import os
import sys

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.simple_resume_analyzer import SimpleResumeAnalyzer

def test_different_resumes():
    """Test analyzer with different resume contents"""
    
    analyzer = SimpleResumeAnalyzer()
    
    # Create test resume contents with very different profiles
    resume1_text = """
John Doe
Senior Python Developer
Email: john.doe@email.com
Phone: 555-0123

EXPERIENCE:
Senior Python Developer (2019-2024)
- Built scalable web applications using Django and Flask
- Designed RESTful APIs serving 1M+ users
- Led team of 5 developers
- Experience with AWS, Docker, Kubernetes
- Machine learning projects using TensorFlow and PyTorch

SKILLS:
Python, Django, Flask, SQL, PostgreSQL, AWS, Docker, Kubernetes, Machine Learning, TensorFlow, PyTorch, REST APIs, Git, Agile

EDUCATION:
Bachelor's in Computer Science
"""

    resume2_text = """
Sarah Smith
Data Analyst
Email: sarah.smith@email.com  
Phone: 555-0456

EXPERIENCE:
Data Analyst (2021-2024)
- Analyzed business data using Excel and Power BI
- Created dashboards and reports for management
- Statistical analysis and data visualization
- Worked with SQL databases
- No programming experience

SKILLS:
Excel, Power BI, Tableau, SQL, Statistics, Data Visualization, Business Analysis, SPSS

EDUCATION:
Bachelor's in Business Administration
"""

    resume3_text = """
Mike Johnson
Java Backend Developer
Email: mike.johnson@email.com
Phone: 555-0789

EXPERIENCE:
Java Developer (2020-2024)
- Developed enterprise Java applications
- Spring Boot microservices architecture
- Oracle database integration
- No Python experience
- Focus on enterprise systems

SKILLS:
Java, Spring Boot, Spring Framework, Oracle, Maven, Jenkins, Enterprise Architecture, Microservices

EDUCATION:
Bachelor's in Software Engineering
"""

    job_text = """
Senior Python Developer Position

We are looking for a Senior Python Developer with the following requirements:

REQUIRED SKILLS:
- 5+ years Python development experience
- Django or Flask framework experience
- RESTful API development
- SQL database experience
- Cloud platforms (AWS/Azure)
- Machine learning experience preferred

RESPONSIBILITIES:
- Lead Python development projects
- Design and implement scalable web applications
- Mentor junior developers
- Work with data science team on ML projects
"""

    print("Testing analyzer with different resume profiles...")
    print("=" * 60)
    
    # Test each resume
    resumes = [
        ("John Doe (Python Expert)", resume1_text),
        ("Sarah Smith (Data Analyst)", resume2_text), 
        ("Mike Johnson (Java Developer)", resume3_text)
    ]
    
    for name, resume_text in resumes:
        print(f"\n--- ANALYZING: {name} ---")
        
        # Clean the text first and show what the analyzer sees
        clean_resume = analyzer._clean_text(resume_text)
        resume_skills = analyzer._extract_skills(clean_resume)
        
        print(f"Clean text length: {len(clean_resume)}")
        print(f"Skills extracted: {list(resume_skills)[:10]}")  # Show first 10 skills
        
        # Perform full analysis
        result = analyzer.analyze_resume(resume_text, job_text)
        
        print(f"Overall Score: {result['overall_score']}")
        print(f"Match Level: {result['match_level']}")
        print(f"Component Scores:")
        for component, score in result['component_scores'].items():
            print(f"  {component}: {score}")
        print(f"Explanation: {result['explanation'][:100]}...")
        
        print("-" * 40)

if __name__ == "__main__":
    test_different_resumes()