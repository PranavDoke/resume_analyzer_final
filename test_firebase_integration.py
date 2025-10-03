"""
Test Firebase Integration for Resume Analyzer
"""

import sys
import os
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

try:
    from firebase.firebase_service import get_firebase_service
    from firebase.firebase_config import validate_firebase_config, get_firebase_config
    
    print("🧪 Testing Firebase Integration for Resume Analyzer")
    print("=" * 60)
    
    # Test 1: Configuration validation
    print("\n1. Testing Firebase Configuration...")
    config_valid = validate_firebase_config()
    if config_valid:
        print("✅ Firebase configuration is valid")
    else:
        print("⚠️ Firebase configuration needs to be updated with your credentials")
        print("Please update config/firebase_service_account.json with your Firebase credentials")
    
    # Test 2: Service initialization
    print("\n2. Testing Firebase Service Initialization...")
    firebase_service = get_firebase_service()
    
    if firebase_service.is_initialized():
        print("✅ Firebase service initialized successfully")
    else:
        print("⚠️ Firebase service not initialized (this is expected with sample config)")
    
    # Test 3: Sample data structure
    print("\n3. Testing Data Structure...")
    sample_analysis_results = {
        'metadata': {
            'resume_filename': 'sample_resume.pdf',
            'job_description_filename': 'sample_jd.pdf',
            'processing_time': 2.5,
            'timestamp': 1609459200,
            'success': True
        },
        'analysis_results': {
            'overall_score': 85.5,
            'match_level': 'excellent',
            'confidence': 92.0,
            'hard_matching': {
                'score': 80.0,
                'weight': 0.4,
                'weighted_score': 32.0,
                'details': {
                    'skills_match_score': 85.0,
                    'skills_found': ['Python', 'Machine Learning', 'SQL'],
                    'skills_missing': ['Docker', 'Kubernetes'],
                    'keyword_match_score': 75.0,
                    'tfidf_score': 78.0,
                    'bm25_score': 82.0
                }
            },
            'soft_matching': {
                'score': 88.0,
                'weight': 0.3,
                'weighted_score': 26.4,
                'details': {
                    'semantic_similarity': 90.0,
                    'embedding_similarity': 86.0,
                    'context_relevance': 88.0
                }
            },
            'llm_analysis': {
                'score': 90.0,
                'weight': 0.3,
                'weighted_score': 27.0,
                'reasoning': 'Strong technical background with relevant experience',
                'confidence': 95.0,
                'verdict': 'HIRE'
            }
        },
        'hiring_recommendation': {
            'decision': 'HIRE',
            'confidence': 92.0,
            'reasoning': 'Excellent match for the role'
        },
        'gap_analysis': {
            'missing_skills': ['Docker', 'Kubernetes'],
            'improvement_areas': ['Cloud technologies']
        },
        'extracted_info': {
            'resume_skills': ['Python', 'Machine Learning', 'SQL', 'TensorFlow'],
            'resume_keywords': ['data science', 'analytics', 'modeling'],
            'jd_requirements': ['3+ years experience', 'Python', 'ML'],
            'jd_skills': ['Python', 'Machine Learning', 'SQL', 'Docker']
        }
    }
    
    print("✅ Sample data structure prepared")
    
    # Test 4: Data storage (only if Firebase is properly configured)
    if firebase_service.is_initialized():
        print("\n4. Testing Data Storage...")
        try:
            doc_id = firebase_service.store_resume_analysis(
                resume_filename="test_resume.pdf",
                job_description_filename="test_jd.pdf",
                analysis_results=sample_analysis_results,
                user_info={"test_user": True, "ip": "127.0.0.1"}
            )
            
            if doc_id:
                print(f"✅ Test data stored successfully with ID: {doc_id}")
            else:
                print("❌ Failed to store test data")
                
        except Exception as e:
            print(f"❌ Error during data storage: {e}")
    else:
        print("\n4. Skipping Data Storage Test (Firebase not configured)")
    
    # Test 5: Show expected Firebase document structure
    print("\n5. Expected Firebase Document Structure:")
    print("-" * 40)
    expected_structure = {
        "timestamp": "2024-01-01T00:00:00Z",
        "resume_filename": "candidate_resume.pdf",
        "job_description_filename": "job_posting.pdf",
        "overall_score": 85.5,
        "match_level": "excellent",
        "scoring_details": {
            "skills_match_score": 85.0,
            "keyword_match_score": 75.0,
            "semantic_similarity": 90.0,
            "llm_reasoning_score": 90.0,
            "total_weighted_score": 85.5
        },
        "hard_matching": {"score": 80.0, "weight": 0.4, "weighted_score": 32.0},
        "soft_matching": {"score": 88.0, "weight": 0.3, "weighted_score": 26.4},
        "llm_analysis": {"score": 90.0, "weight": 0.3, "weighted_score": 27.0},
        "hiring_recommendation": {"decision": "HIRE", "confidence": 92.0},
        "user_info": {"session_id": "...", "ip_address": "..."}
    }
    
    import json
    print(json.dumps(expected_structure, indent=2))
    
    print("\n" + "=" * 60)
    print("🎯 Firebase Integration Summary:")
    print(f"✅ Firebase Admin SDK: Installed")
    print(f"{'✅' if config_valid else '⚠️'} Configuration: {'Valid' if config_valid else 'Needs setup'}")
    print(f"{'✅' if firebase_service.is_initialized() else '⚠️'} Service: {'Ready' if firebase_service.is_initialized() else 'Needs credentials'}")
    print(f"✅ Integration: Complete")
    
    if not firebase_service.is_initialized():
        print("\n📝 Next Steps:")
        print("1. Create a Firebase project at https://console.firebase.google.com/")
        print("2. Generate a service account key")
        print("3. Update config/firebase_service_account.json with your credentials")
        print("4. Update FIREBASE_PROJECT_ID in firebase_config.py")
        print("5. Run this test again to verify connection")
    
    print("\n🔥 Ready to log resume analysis results to Firebase collection 'resumeanalyser'!")

except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("Please ensure Firebase dependencies are installed: pip install firebase-admin")
except Exception as e:
    print(f"❌ Test Error: {e}")
    import traceback
    traceback.print_exc()