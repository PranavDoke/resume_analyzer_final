#!/usr/bin/env python3
"""
Resume Analyzer Deployment Helper Script
Prepares the application for various deployment scenarios
"""

import os
import subprocess
import sys
from pathlib import Path

def check_requirements():
    """Check if all required dependencies are available"""
    print("🔍 Checking requirements...")
    
    required_files = [
        "web_app/app.py",
        "requirements.txt",
        "src/simple_resume_analyzer.py"
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    
    print("✅ All required files present")
    return True

def setup_environment():
    """Setup local environment for testing deployment"""
    print("🛠️ Setting up environment...")
    
    try:
        # Install requirements
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        
        # Download spaCy model
        subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"], check=True)
        
        print("✅ Environment setup complete")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error setting up environment: {e}")
        return False

def test_local_deployment():
    """Test the application locally"""
    print("🧪 Testing local deployment...")
    
    try:
        # Run a quick import test
        subprocess.run([
            sys.executable, "-c", 
            "import streamlit; from src.simple_resume_analyzer import ResumeAnalyzer; print('✅ Imports successful')"
        ], check=True, cwd=".")
        
        print("✅ Local deployment test passed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Local deployment test failed: {e}")
        return False

def create_docker_files():
    """Create Docker deployment files"""
    print("🐳 Creating Docker files...")
    
    dockerfile_content = """FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    build-essential \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements-deployment.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy model
RUN python -m spacy download en_core_web_sm

# Copy application code
COPY . .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run the application
CMD ["streamlit", "run", "web_app/app.py", "--server.headless", "true", "--server.port", "8501", "--server.address", "0.0.0.0"]
"""
    
    dockerignore_content = """.git
.gitignore
README.md
DEPLOYMENT.md
*.pyc
__pycache__
.pytest_cache
.coverage
.env
*.log
temp_uploads/
test_data/
sample_data/
"""
    
    with open("Dockerfile", "w") as f:
        f.write(dockerfile_content)
    
    with open(".dockerignore", "w") as f:
        f.write(dockerignore_content)
    
    print("✅ Docker files created")

def prepare_for_streamlit_cloud():
    """Prepare files for Streamlit Cloud deployment"""
    print("☁️ Preparing for Streamlit Cloud...")
    
    # Create packages.txt for system dependencies
    packages_content = """build-essential
"""
    
    with open("packages.txt", "w") as f:
        f.write(packages_content)
    
    print("✅ Streamlit Cloud preparation complete")
    print("📋 Next steps:")
    print("   1. Push your code to GitHub")
    print("   2. Go to share.streamlit.io")
    print("   3. Connect your GitHub repo")
    print("   4. Set main file: web_app/app.py")
    print("   5. Add your API keys in Secrets")

def main():
    """Main deployment preparation function"""
    print("🚀 Resume Analyzer Deployment Helper")
    print("=" * 50)
    
    if not check_requirements():
        return
    
    print("\\nChoose deployment option:")
    print("1. Streamlit Cloud (Recommended)")
    print("2. Local testing")
    print("3. Docker deployment")
    print("4. Full setup (all options)")
    
    choice = input("\\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        prepare_for_streamlit_cloud()
    elif choice == "2":
        if setup_environment():
            test_local_deployment()
    elif choice == "3":
        create_docker_files()
        print("✅ Docker files created. Build with: docker build -t resume-analyzer .")
    elif choice == "4":
        setup_environment()
        test_local_deployment()
        create_docker_files()
        prepare_for_streamlit_cloud()
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()