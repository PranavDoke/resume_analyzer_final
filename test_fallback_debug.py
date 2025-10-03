#!/usr/bin/env python3
"""
Debug script to test the fallback mechanism specifically
"""

import os
import sys

# Add src to path
sys.path.append('src')

from resume_analyzer import ResumeAnalyzer

def test_fallback_directly():
    """Test the fallback mechanism directly"""
    
    analyzer = ResumeAnalyzer()
    
    # Test one case with detailed debugging
    print("Testing fallback mechanism directly...")
    
    # Parse documents manually first
    resume_data = analyzer.document_parser.parse_document('test_data/strong_python_candidate.txt')
    jd_data = analyzer.document_parser.parse_document('test_data/senior_python_developer.txt')
    
    print(f"Resume data keys: {list(resume_data.keys())}")
    print(f"JD data keys: {list(jd_data.keys())}")
    
    # Test if we have text content
    for key, value in resume_data.items():
        if isinstance(value, str) and value:
            print(f"Resume {key}: {len(value)} chars - {value[:100]}...")
    
    for key, value in jd_data.items():
        if isinstance(value, str) and value:
            print(f"JD {key}: {len(value)} chars - {value[:100]}...")
    
    # Call fallback directly
    print("\nCalling fallback directly...")
    fallback_result = analyzer._use_simple_analyzer_fallback(resume_data, jd_data)
    
    print(f"Fallback result: {fallback_result}")
    
    if fallback_result and 'simple_analysis' in fallback_result:
        simple_result = fallback_result['simple_analysis']
        print(f"Simple analysis overall score: {simple_result.get('overall_score', 'N/A')}")
        print(f"Component scores: {simple_result.get('component_scores', {})}")

if __name__ == "__main__":
    test_fallback_directly()