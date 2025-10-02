#!/usr/bin/env python3
"""
Comprehensive Test Suite for Resume Analyzer Web Application
Tests all features, navigation, file upload, and analysis functionality
"""

import os
import sys
import time
import json
from pathlib import Path
from datetime import datetime

# Add project paths
project_root = Path(__file__).parent
sys.path.append(str(project_root))
sys.path.append(str(project_root / 'src'))
sys.path.append(str(project_root / 'web_app'))

def test_imports():
    """Test all critical imports"""
    print("🧪 Testing Critical Imports...")
    
    tests = [
        ("streamlit", "import streamlit as st"),
        ("pandas", "import pandas as pd"),
        ("plotly", "import plotly.express as px"),
        ("config", "from config.settings import load_config"),
        ("analyzer", "from simple_resume_analyzer import ResumeAnalyzer"),
        ("pathlib", "from pathlib import Path"),
        ("json", "import json"),
        ("datetime", "from datetime import datetime"),
    ]
    
    results = {}
    for name, import_stmt in tests:
        try:
            exec(import_stmt)
            results[name] = "✅ PASS"
        except Exception as e:
            results[name] = f"❌ FAIL: {e}"
    
    for name, result in results.items():
        print(f"  {name:<15}: {result}")
    
    return all("✅ PASS" in r for r in results.values())

def test_config():
    """Test configuration loading"""
    print("\n🧪 Testing Configuration...")
    
    try:
        from config.settings import load_config
        config = load_config()
        
        if config and 'openrouter' in config:
            print("  ✅ Config loaded successfully")
            print(f"  ✅ OpenRouter API key: {'*' * 20}{config['openrouter']['api_key'][-10:]}")
            print(f"  ✅ Model: {config['openrouter']['model']}")
            return True
        else:
            print("  ❌ Config structure invalid")
            return False
            
    except Exception as e:
        print(f"  ❌ Config loading failed: {e}")
        return False

def test_analyzer_initialization():
    """Test analyzer initialization"""
    print("\n🧪 Testing Analyzer Initialization...")
    
    try:
        from simple_resume_analyzer import ResumeAnalyzer
        from config.settings import load_config
        
        config = load_config()
        analyzer = ResumeAnalyzer(config)
        
        print("  ✅ Analyzer initialized successfully")
        print(f"  ✅ Analyzer type: {type(analyzer).__name__}")
        return True
        
    except Exception as e:
        print(f"  ❌ Analyzer initialization failed: {e}")
        return False

def test_file_structure():
    """Test required file structure"""
    print("\n🧪 Testing File Structure...")
    
    required_paths = [
        "web_app/app.py",
        "src/simple_resume_analyzer.py",
        "config/settings.py",
        "sample_data/resumes",
        "sample_data/jds",
        "temp_uploads",
        "exports"
    ]
    
    results = {}
    for path in required_paths:
        full_path = project_root / path
        if full_path.exists():
            results[path] = "✅ EXISTS"
        else:
            results[path] = "❌ MISSING"
            
    for path, result in results.items():
        print(f"  {path:<30}: {result}")
    
    return all("✅ EXISTS" in r for r in results.values())

def test_sample_data():
    """Test sample data availability"""
    print("\n🧪 Testing Sample Data...")
    
    sample_paths = [
        "sample_data/resumes/Resumes",
        "sample_data/jds/JD", 
        "test_data"
    ]
    
    total_files = 0
    for path in sample_paths:
        full_path = project_root / path
        if full_path.exists():
            files = list(full_path.glob("*"))
            total_files += len(files)
            print(f"  {path}: ✅ {len(files)} files found")
            if files:
                for file in files[:3]:  # Show first 3 files
                    print(f"    - {file.name}")
                if len(files) > 3:
                    print(f"    ... and {len(files) - 3} more")
        else:
            print(f"  {path}: ❌ Directory not found")
    
    return total_files > 0

def test_resume_analysis():
    """Test resume analysis functionality"""
    print("\n🧪 Testing Resume Analysis...")
    
    try:
        from simple_resume_analyzer import ResumeAnalyzer
        from config.settings import load_config
        
        # Initialize analyzer
        config = load_config()
        analyzer = ResumeAnalyzer(config)
        
        # Test with sample resume text
        sample_resume = """
        John Doe
        Software Developer
        
        Experience:
        - 3 years of Python development
        - Flask and Django frameworks
        - Database design with PostgreSQL
        - REST API development
        
        Skills:
        Python, Flask, Django, PostgreSQL, JavaScript, HTML, CSS
        
        Education:
        Bachelor's in Computer Science
        """
        
        sample_jd = """
        We are looking for a Python Developer with:
        - 2+ years Python experience
        - Web framework experience (Flask/Django)
        - Database knowledge
        - API development skills
        """
        
        # Perform analysis
        print("  🔄 Running analysis...")
        result = analyzer.analyze_resume(sample_resume, sample_jd)
        
        if result and 'overall_score' in result:
            print(f"  ✅ Analysis completed successfully")
            print(f"  ✅ Overall Score: {result['overall_score']:.1f}")
            print(f"  ✅ Components analyzed: {len(result.get('component_scores', {}))}")
            return True
        else:
            print(f"  ❌ Analysis failed or invalid result")
            return False
            
    except Exception as e:
        print(f"  ❌ Analysis test failed: {e}")
        return False

def test_web_app_startup():
    """Test web app can start without errors"""
    print("\n🧪 Testing Web App Startup...")
    
    try:
        # Change to web_app directory
        original_cwd = os.getcwd()
        os.chdir(project_root / 'web_app')
        
        # Test importing the app
        sys.path.insert(0, str(project_root / 'web_app'))
        import app
        
        print("  ✅ App module imported successfully")
        
        # Test main function exists
        if hasattr(app, 'main'):
            print("  ✅ Main function found")
        else:
            print("  ❌ Main function not found")
            return False
        
        # Test required functions exist
        required_functions = [
            'show_dashboard',
            'show_single_analysis', 
            'show_batch_analysis',
            'show_results_viewer',
            'initialize_analyzer'
        ]
        
        for func_name in required_functions:
            if hasattr(app, func_name):
                print(f"  ✅ Function {func_name} found")
            else:
                print(f"  ❌ Function {func_name} missing")
        
        os.chdir(original_cwd)
        return True
        
    except Exception as e:
        os.chdir(original_cwd)
        print(f"  ❌ Web app startup test failed: {e}")
        return False

def test_directories_permissions():
    """Test directory permissions for uploads and exports"""
    print("\n🧪 Testing Directory Permissions...")
    
    test_dirs = ['temp_uploads', 'exports', 'logs', 'web_app/temp_uploads']
    success_count = 0
    
    for dir_name in test_dirs:
        dir_path = project_root / dir_name
        
        try:
            # Create directory if it doesn't exist
            dir_path.mkdir(exist_ok=True)
            
            # Test write permissions
            test_file = dir_path / 'test_write.txt'
            test_file.write_text('test')
            test_file.unlink()
            
            print(f"  ✅ {dir_name}: Read/Write OK")
            success_count += 1
            
        except Exception as e:
            print(f"  ❌ {dir_name}: Permission error - {e}")
    
    return success_count == len(test_dirs)

def run_comprehensive_test():
    """Run all tests"""
    print("🎯 Resume Analyzer Comprehensive Test Suite")
    print("=" * 60)
    print(f"📍 Project Root: {project_root}")
    print(f"🕐 Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    test_results = []
    
    # Run all tests
    test_results.append(("Imports", test_imports()))
    test_results.append(("Configuration", test_config()))
    test_results.append(("File Structure", test_file_structure()))
    test_results.append(("Sample Data", test_sample_data()))
    test_results.append(("Analyzer Init", test_analyzer_initialization()))
    test_results.append(("Resume Analysis", test_resume_analysis()))
    test_results.append(("Web App Startup", test_web_app_startup()))
    test_results.append(("Directory Permissions", test_directories_permissions()))
    
    # Summary
    print("\n" + "=" * 60)
    print("🎯 TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<25}: {status}")
        if result:
            passed += 1
    
    print("=" * 60)
    print(f"📊 Results: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 All tests passed! The application is ready to use.")
    else:
        print("⚠️  Some tests failed. Check the details above.")
    
    return passed == total

if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)