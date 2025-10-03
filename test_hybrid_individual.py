#!/usr/bin/env python3
"""
Test script to verify that individual resumes now produce different results
"""

import os
import sys

# Add src to path
sys.path.append('src')

from resume_analyzer import ResumeAnalyzer

def test_individual_results():
    """Test that different resumes produce different results"""
    
    analyzer = ResumeAnalyzer()
    
    # Test data
    test_cases = [
        {
            'name': 'Strong Python Candidate',
            'resume_path': 'test_data/strong_python_candidate.txt',
            'jd_path': 'test_data/senior_python_developer.txt'
        },
        {
            'name': 'Junior Candidate',
            'resume_path': 'test_data/junior_candidate.txt',
            'jd_path': 'test_data/senior_python_developer.txt'
        },
        {
            'name': 'Unrelated Candidate',
            'resume_path': 'test_data/unrelated_candidate.txt',
            'jd_path': 'test_data/senior_python_developer.txt'
        }
    ]
    
    results = []
    
    print("Testing individual resume analysis with hybrid system...")
    print("=" * 60)
    
    for test_case in test_cases:
        print(f"\nAnalyzing: {test_case['name']}")
        print("-" * 40)
        
        try:
            result = analyzer.analyze_resume_for_job(
                test_case['resume_path'],
                test_case['jd_path']
            )
            
            if result:
                # Extract score from correct location
                score = result.get('analysis_results', {}).get('overall_score', 0)
                method = result.get('analysis_results', {}).get('analysis_method', 'unknown')
                
                # Check if fallback was used
                fallback_used = 'fallback' in method or 'simple' in str(result).lower()
                
                print(f"✅ Score: {score:.1f}")
                print(f"   Method: {method}")
                print(f"   Fallback Used: {fallback_used}")
                
                # Print component scores for verification  
                detailed_results = result.get('detailed_results', {})
                if 'hard_matching' in detailed_results:
                    hard_results = detailed_results['hard_matching']
                    print(f"   Hard Matching Score: {hard_results.get('overall_score', 0):.1f}")
                if 'soft_matching' in detailed_results:
                    soft_results = detailed_results['soft_matching']
                    print(f"   Soft Matching Score: {soft_results.get('combined_semantic_score', 0):.1f}")
                
                # Check analysis results for more details
                analysis_results = result.get('analysis_results', {})
                print(f"   Match Level: {analysis_results.get('match_level', 'unknown')}")
                print(f"   Confidence: {analysis_results.get('confidence', 0):.2f}")
                
                results.append({
                    'name': test_case['name'],
                    'score': score,
                    'method': method,
                    'fallback_used': fallback_used
                })
                
            else:
                print(f"❌ Analysis failed")
                results.append({
                    'name': test_case['name'],
                    'score': 0,
                    'method': 'failed',
                    'fallback_used': False
                })
                
        except Exception as e:
            print(f"❌ Error: {e}")
            results.append({
                'name': test_case['name'],
                'score': 0,
                'method': 'error',
                'fallback_used': False
            })
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY - Individual Analysis Results")
    print("=" * 60)
    
    scores = [r['score'] for r in results if r['score'] > 0]
    
    if len(set(scores)) > 1:
        print("✅ SUCCESS: Different resumes produced different scores!")
        for result in results:
            print(f"   {result['name']}: {result['score']:.1f} ({result['method']})")
        
        print(f"\nScore range: {min(scores):.1f} - {max(scores):.1f}")
        print(f"Score variation: {max(scores) - min(scores):.1f} points")
        
    else:
        print("❌ ISSUE: All resumes still produce the same scores")
        for result in results:
            print(f"   {result['name']}: {result['score']:.1f}")
    
    # Check if fallback is working
    fallback_count = sum(1 for r in results if r['fallback_used'])
    print(f"\nFallback system used: {fallback_count}/{len(results)} cases")
    
    return results

if __name__ == "__main__":
    results = test_individual_results()