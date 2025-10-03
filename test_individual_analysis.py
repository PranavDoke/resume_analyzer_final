"""
Test the fixed analyzer with different resume content to verify individualized results
"""
import sys
import os
import tempfile

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_test_files():
    """Create test resume and job files with different content"""
    
    # Python expert resume
    python_resume = """
    John Smith
    Senior Python Developer
    john.smith@email.com | 555-123-4567
    
    EXPERIENCE:
    Senior Python Developer at TechCorp (2020-2024)
    - Developed scalable web applications using Django and Flask
    - Built REST APIs serving 1M+ daily requests
    - Led development of machine learning models using TensorFlow
    - Managed AWS infrastructure with Docker and Kubernetes
    - Mentored team of 5 junior developers
    
    Python Developer at StartupXYZ (2018-2020)
    - Created data processing pipelines using Pandas and NumPy
    - Implemented automated testing with pytest
    - Worked with PostgreSQL and Redis databases
    
    SKILLS:
    Python, Django, Flask, FastAPI, PostgreSQL, MongoDB, AWS, Docker, 
    Kubernetes, Machine Learning, TensorFlow, PyTorch, Pandas, NumPy, 
    REST APIs, Git, Agile, Scrum
    
    EDUCATION:
    Bachelor of Computer Science, MIT (2014-2018)
    """
    
    # Data analyst resume (different profile)
    analyst_resume = """
    Sarah Johnson
    Business Data Analyst
    sarah.johnson@email.com | 555-987-6543
    
    EXPERIENCE:
    Senior Data Analyst at BusinessCorp (2021-2024)
    - Analyzed sales data using Excel and Power BI
    - Created executive dashboards and KPI reports
    - Performed statistical analysis using SPSS
    - Worked with SQL databases for data extraction
    - Presented insights to C-level executives
    
    Data Analyst at ConsultingFirm (2019-2021)
    - Built financial models in Excel
    - Created Tableau visualizations
    - Analyzed customer behavior data
    - No programming experience
    
    SKILLS:
    Excel, Power BI, Tableau, SQL, SPSS, Statistical Analysis, 
    Data Visualization, Business Intelligence, Financial Modeling, 
    Report Generation, Presentation Skills
    
    EDUCATION:
    Bachelor of Business Administration, Local University (2015-2019)
    """
    
    # Job description for Python developer
    job_desc = """
    Senior Python Developer Position
    
    COMPANY: TechInnovate Solutions
    
    JOB REQUIREMENTS:
    - 5+ years of Python development experience
    - Strong experience with Django or Flask frameworks
    - REST API development and microservices architecture
    - Cloud platforms experience (AWS, Azure, or GCP)
    - Database experience with PostgreSQL or MongoDB
    - Machine learning experience preferred
    - Docker and Kubernetes knowledge
    - Strong problem-solving and leadership skills
    
    RESPONSIBILITIES:
    - Lead Python development projects
    - Design and implement scalable web applications
    - Mentor junior developers
    - Collaborate with data science team on ML projects
    - Ensure code quality and best practices
    
    NICE TO HAVE:
    - TensorFlow or PyTorch experience
    - DevOps and CI/CD knowledge
    - Agile/Scrum methodology experience
    """
    
    # Create temporary files
    temp_dir = tempfile.mkdtemp()
    
    files = {}
    files['python_resume'] = os.path.join(temp_dir, 'python_expert.txt')
    files['analyst_resume'] = os.path.join(temp_dir, 'data_analyst.txt') 
    files['job_desc'] = os.path.join(temp_dir, 'python_job.txt')
    
    with open(files['python_resume'], 'w') as f:
        f.write(python_resume)
    
    with open(files['analyst_resume'], 'w') as f:
        f.write(analyst_resume)
        
    with open(files['job_desc'], 'w') as f:
        f.write(job_desc)
    
    return files

def test_analyzer():
    """Test the analyzer with different resumes"""
    
    try:
        # Import the full analyzer
        from src.resume_analyzer import ResumeAnalyzer
        from config.settings import get_config
        
        print("🔄 Initializing Resume Analyzer...")
        config = get_config()
        analyzer = ResumeAnalyzer(config)
        
        # Create test files
        print("📝 Creating test files...")
        test_files = create_test_files()
        
        print("🧪 Testing Python Expert Resume...")
        python_results = analyzer.analyze_resume_for_job(
            test_files['python_resume'], 
            test_files['job_desc'], 
            save_to_db=False
        )
        
        print("🧪 Testing Data Analyst Resume...")
        analyst_results = analyzer.analyze_resume_for_job(
            test_files['analyst_resume'],
            test_files['job_desc'], 
            save_to_db=False
        )
        
        # Compare results
        print("\n" + "="*60)
        print("🔍 ANALYSIS RESULTS COMPARISON")
        print("="*60)
        
        python_score = python_results['analysis_results']['overall_score']
        analyst_score = analyst_results['analysis_results']['overall_score']
        
        print(f"📊 Python Expert Score: {python_score:.2f}")
        print(f"📊 Data Analyst Score: {analyst_score:.2f}")
        print(f"📊 Score Difference: {abs(python_score - analyst_score):.2f}")
        
        print(f"\n🎯 Python Expert Match Level: {python_results['analysis_results']['match_level']}")
        print(f"🎯 Data Analyst Match Level: {analyst_results['analysis_results']['match_level']}")
        
        # Check if results are different
        if abs(python_score - analyst_score) > 10:
            print("\n✅ SUCCESS: Analyzer produces different scores for different resumes!")
            print(f"   The Python expert scored {python_score:.1f} vs Data analyst {analyst_score:.1f}")
        else:
            print("\n❌ ISSUE: Scores are too similar - analyzer may not be differentiating properly")
            
        # Show detailed breakdown
        print(f"\n📋 Python Expert Skills: {python_results['resume_data'].get('skills', [])[:5]}")
        print(f"📋 Data Analyst Skills: {analyst_results['resume_data'].get('skills', [])[:5]}")
        
        # Clean up
        import shutil
        shutil.rmtree(os.path.dirname(test_files['python_resume']))
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Testing Resume Analyzer with Individual Analysis...")
    success = test_analyzer()
    if success:
        print("\n🎉 Test completed successfully!")
    else:
        print("\n💥 Test failed - check the errors above")