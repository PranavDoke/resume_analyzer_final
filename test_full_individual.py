"""
Test the full enterprise analyzer with different resumes to check if it produces unique results
"""
import sys
import os
import tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_test_resumes():
    """Create test resume files with very different content"""
    
    # Expert Python Developer Resume
    python_expert = """
    ALEX RODRIGUEZ
    Senior Python Developer | Machine Learning Engineer
    alex.rodriguez@email.com | (555) 123-4567 | LinkedIn: /in/alexrodriguez
    
    PROFESSIONAL SUMMARY
    Highly skilled Senior Python Developer with 7+ years of experience in developing scalable web applications,
    machine learning systems, and data processing pipelines. Expert in Django, Flask, AWS, and modern ML frameworks.
    
    TECHNICAL SKILLS
    • Programming: Python, JavaScript, SQL, Java, Go
    • Frameworks: Django, Flask, FastAPI, React, Vue.js
    • Machine Learning: TensorFlow, PyTorch, Scikit-learn, Pandas, NumPy
    • Cloud Platforms: AWS (EC2, S3, Lambda, RDS), Azure, Google Cloud Platform
    • Databases: PostgreSQL, MongoDB, Redis, Elasticsearch
    • DevOps: Docker, Kubernetes, Jenkins, Git, CI/CD
    • Tools: Jupyter, Apache Spark, Kafka, RabbitMQ
    
    PROFESSIONAL EXPERIENCE
    
    Senior Python Developer | TechCorp Inc. | 2020 - Present
    • Lead development of high-traffic web applications serving 2M+ users daily using Django and PostgreSQL
    • Built and deployed ML models for recommendation systems increasing user engagement by 35%
    • Designed and implemented microservices architecture using Docker and Kubernetes
    • Mentored team of 6 junior developers and conducted code reviews
    • Optimized database queries reducing response times by 60%
    
    Python Developer | DataSolutions Ltd. | 2018 - 2020
    • Developed data processing pipelines handling 100GB+ daily using Apache Spark and Python
    • Created REST APIs using Flask serving 10K+ requests per minute
    • Implemented automated testing achieving 95% code coverage
    • Worked with cross-functional teams in Agile/Scrum environment
    
    Junior Python Developer | StartupXYZ | 2017 - 2018
    • Built web scraping tools processing 1M+ records daily
    • Developed Django applications with Redis caching
    • Participated in daily standups and sprint planning
    
    EDUCATION
    Master of Science in Computer Science | Stanford University | 2017
    Bachelor of Science in Software Engineering | UC Berkeley | 2015
    
    CERTIFICATIONS
    • AWS Certified Solutions Architect
    • Google Cloud Professional Data Engineer
    • Certified Kubernetes Administrator (CKA)
    
    PROJECTS
    • E-commerce Platform: Built full-stack application using Django, React, and PostgreSQL
    • ML Prediction System: Developed neural network for stock price prediction using TensorFlow
    • Real-time Chat Application: Created WebSocket-based chat using Python and Redis
    """
    
    # Junior Marketing Analyst Resume (completely different field)
    marketing_analyst = """
    SARAH JOHNSON
    Marketing Analyst | Digital Marketing Specialist
    sarah.johnson@email.com | (555) 987-6543 | LinkedIn: /in/sarahjohnson
    
    PROFESSIONAL SUMMARY
    Results-driven Marketing Analyst with 2 years of experience in digital marketing campaigns,
    social media management, and brand strategy. Skilled in market research, content creation, and campaign optimization.
    
    CORE COMPETENCIES
    • Digital Marketing: SEO, SEM, Social Media Marketing, Email Marketing
    • Analytics Tools: Google Analytics, Facebook Insights, Hootsuite, Mailchimp
    • Design Software: Canva, Adobe Photoshop, Illustrator (Basic)
    • Office Suite: Microsoft Excel, PowerPoint, Word, Google Workspace
    • Research: Market Research, Competitor Analysis, Consumer Behavior
    • Communication: Content Writing, Copywriting, Presentation Skills
    
    PROFESSIONAL EXPERIENCE
    
    Marketing Analyst | BrandBoost Agency | 2022 - Present
    • Managed social media accounts for 15+ clients across Instagram, Facebook, and Twitter
    • Increased client engagement rates by 40% through targeted content strategies
    • Created weekly performance reports using Google Analytics and social media insights
    • Conducted market research for new product launches and brand positioning
    • Collaborated with design team to create marketing materials and advertisements
    
    Junior Marketing Coordinator | LocalBiz Solutions | 2021 - 2022
    • Assisted in planning and executing digital marketing campaigns for small businesses
    • Wrote blog posts and social media content increasing website traffic by 25%
    • Organized promotional events and trade show participation
    • Maintained customer databases and email marketing lists
    
    Marketing Intern | Creative Media Group | Summer 2021
    • Supported senior marketers in campaign development and execution
    • Conducted competitive analysis and market research
    • Created social media content and managed posting schedules
    • Learned basic graphic design and video editing skills
    
    EDUCATION
    Bachelor of Arts in Marketing | University of California, Los Angeles | 2021
    Minor in Communications
    
    CERTIFICATIONS
    • Google Analytics Certified
    • Facebook Blueprint Certification
    • HubSpot Content Marketing Certification
    
    PROJECTS
    • Social Media Campaign: Led Instagram campaign for local restaurant resulting in 200% follower increase
    • Market Research Study: Conducted consumer behavior analysis for startup beauty brand
    • Email Marketing Campaign: Designed email sequence achieving 15% open rate improvement
    
    AWARDS
    • Dean's List (3 semesters)
    • Outstanding Marketing Student Award 2021
    """
    
    # Job Description for Senior Python Developer
    job_description = """
    SENIOR PYTHON DEVELOPER
    TechInnovate Solutions | San Francisco, CA | Full-time
    
    COMPANY OVERVIEW
    TechInnovate Solutions is a leading technology company specializing in AI-powered enterprise solutions.
    We serve Fortune 500 companies and process billions of data points daily.
    
    JOB DESCRIPTION
    We are seeking a highly skilled Senior Python Developer to join our engineering team. The ideal candidate
    will have extensive experience in Python development, machine learning, and cloud technologies.
    
    KEY RESPONSIBILITIES
    • Design and develop scalable Python applications and APIs
    • Build and deploy machine learning models for production systems
    • Lead architecture decisions for microservices and distributed systems
    • Mentor junior developers and conduct technical code reviews
    • Collaborate with product managers and data scientists on feature development
    • Optimize application performance and ensure high availability
    • Implement CI/CD pipelines and automated testing frameworks
    
    REQUIRED QUALIFICATIONS
    • 5+ years of professional Python development experience
    • Strong expertise in Django, Flask, or FastAPI frameworks
    • Experience with machine learning libraries (TensorFlow, PyTorch, Scikit-learn)
    • Proficiency in cloud platforms (AWS, Azure, or GCP)
    • Solid understanding of databases (PostgreSQL, MongoDB, Redis)
    • Experience with containerization (Docker) and orchestration (Kubernetes)
    • Knowledge of version control (Git) and CI/CD pipelines
    • Strong problem-solving skills and ability to work in Agile environment
    
    PREFERRED QUALIFICATIONS
    • Master's degree in Computer Science or related field
    • Experience with big data technologies (Spark, Kafka, Hadoop)
    • Knowledge of DevOps practices and tools
    • AWS/Azure/GCP certifications
    • Experience leading technical teams
    • Contributions to open-source projects
    
    TECHNICAL REQUIREMENTS
    • Python 3.x expertise
    • RESTful API design and development
    • Microservices architecture
    • Database design and optimization
    • Unit testing and TDD practices
    • Performance monitoring and optimization
    
    WHAT WE OFFER
    • Competitive salary: $150,000 - $200,000 based on experience
    • Comprehensive health, dental, and vision insurance
    • 401(k) with company matching
    • Flexible work arrangements and remote work options
    • Professional development budget and conference attendance
    • Stock options and performance bonuses
    • Collaborative and innovative work environment
    """
    
    # Create temporary files
    temp_dir = tempfile.mkdtemp()
    
    files = {}
    files['python_expert'] = os.path.join(temp_dir, 'alex_python_senior.txt')
    files['marketing_analyst'] = os.path.join(temp_dir, 'sarah_marketing.txt')
    files['job_description'] = os.path.join(temp_dir, 'senior_python_job.txt')
    
    with open(files['python_expert'], 'w', encoding='utf-8') as f:
        f.write(python_expert)
    
    with open(files['marketing_analyst'], 'w', encoding='utf-8') as f:
        f.write(marketing_analyst)
        
    with open(files['job_description'], 'w', encoding='utf-8') as f:
        f.write(job_description)
    
    return files

def test_full_enterprise_analyzer():
    """Test the full enterprise analyzer with different resumes"""
    
    try:
        print("🔄 Testing Full Enterprise Analyzer with Different Resumes...")
        
        # Import the full analyzer
        from src.resume_analyzer import ResumeAnalyzer
        from config.settings import get_config
        
        config = get_config()
        analyzer = ResumeAnalyzer(config)
        
        print("✅ Full enterprise analyzer initialized")
        
        # Create test files
        test_files = create_test_resumes()
        print("📝 Created test resume files")
        
        print("\n" + "="*70)
        print("🧪 TESTING PYTHON EXPERT vs PYTHON JOB")
        print("="*70)
        
        python_results = analyzer.analyze_resume_for_job(
            test_files['python_expert'], 
            test_files['job_description'], 
            save_to_db=False
        )
        
        python_score = python_results['analysis_results']['overall_score']
        python_match = python_results['analysis_results']['match_level']
        python_name = python_results['resume_data'].get('candidate_name', 'Unknown')
        python_skills = python_results['resume_data'].get('skills', [])
        
        print(f"👤 Candidate: {python_name}")
        print(f"📊 Overall Score: {python_score:.2f}")
        print(f"🎯 Match Level: {python_match}")
        print(f"🔧 Skills Found: {len(python_skills)} ({', '.join(python_skills[:5])}...)")
        
        print("\n" + "="*70)
        print("🧪 TESTING MARKETING ANALYST vs PYTHON JOB")
        print("="*70)
        
        marketing_results = analyzer.analyze_resume_for_job(
            test_files['marketing_analyst'],
            test_files['job_description'], 
            save_to_db=False
        )
        
        marketing_score = marketing_results['analysis_results']['overall_score']
        marketing_match = marketing_results['analysis_results']['match_level']
        marketing_name = marketing_results['resume_data'].get('candidate_name', 'Unknown')
        marketing_skills = marketing_results['resume_data'].get('skills', [])
        
        print(f"👤 Candidate: {marketing_name}")
        print(f"📊 Overall Score: {marketing_score:.2f}")
        print(f"🎯 Match Level: {marketing_match}")
        print(f"🔧 Skills Found: {len(marketing_skills)} ({', '.join(marketing_skills[:5])}...)")
        
        print("\n" + "="*70)
        print("📈 ANALYSIS COMPARISON")
        print("="*70)
        
        score_difference = abs(python_score - marketing_score)
        print(f"Score Difference: {score_difference:.2f} points")
        
        # Check detailed results
        print(f"\nPython Expert Detailed Scores:")
        hard_matching = python_results['detailed_results'].get('hard_matching', {})
        print(f"  - Hard Matching: {hard_matching.get('overall_score', 0):.1f}")
        print(f"  - Skills Score: {hard_matching.get('skills_score', 0):.1f}")
        print(f"  - Keywords Score: {hard_matching.get('keyword_score', 0):.1f}")
        
        print(f"\nMarketing Analyst Detailed Scores:")
        hard_matching_m = marketing_results['detailed_results'].get('hard_matching', {})
        print(f"  - Hard Matching: {hard_matching_m.get('overall_score', 0):.1f}")
        print(f"  - Skills Score: {hard_matching_m.get('skills_score', 0):.1f}")
        print(f"  - Keywords Score: {hard_matching_m.get('keyword_score', 0):.1f}")
        
        # Determine if working correctly
        if score_difference > 15 and python_score > marketing_score:
            print(f"\n✅ SUCCESS: Analyzer correctly differentiates!")
            print(f"   Python Expert: {python_score:.1f} > Marketing Analyst: {marketing_score:.1f}")
            success = True
        else:
            print(f"\n❌ ISSUE: Scores too similar or incorrect ranking")
            print(f"   Expected: Python Expert > Marketing Analyst")
            print(f"   Actual: Python Expert {python_score:.1f}, Marketing Analyst {marketing_score:.1f}")
            success = False
        
        # Clean up
        import shutil
        shutil.rmtree(os.path.dirname(test_files['python_expert']))
        
        return success
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Testing Full Enterprise Resume Analyzer for Individual Results...")
    success = test_full_enterprise_analyzer()
    if success:
        print("\n🎉 Full enterprise analyzer is working correctly!")
    else:
        print("\n💥 Full enterprise analyzer needs fixes!")