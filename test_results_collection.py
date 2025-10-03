#!/usr/bin/env python3
"""
Quick test to verify Firebase integration stores data in 'results' collection
"""

import sys
import os
sys.path.append('src')

from firebase.firebase_service import FirebaseService
from firebase.firebase_config import FIREBASE_CONFIG

def main():
    print("🔥 Testing Firebase Results Collection")
    print("=" * 50)
    
    # Check configuration
    print(f"📋 Collection Name: {FIREBASE_CONFIG['collection_name']}")
    print(f"🚀 Project ID: {FIREBASE_CONFIG['project_id']}")
    
    # Initialize Firebase service
    try:
        firebase_service = FirebaseService()
        print("✅ Firebase service initialized")
    except Exception as e:
        print(f"❌ Firebase initialization failed: {e}")
        return
    
    # Test data to store
    test_data = {
        "test_type": "collection_verification",
        "timestamp": "2024-01-02T10:00:00Z",
        "resume_filename": "test_resume.pdf",
        "job_description_filename": "test_job.pdf",
        "overall_score": 92.5,
        "match_level": "excellent",
        "collection_test": True,
        "verification_message": "Testing if data goes to 'results' collection"
    }
    
    # Store the data using the correct method signature
    try:
        document_id = firebase_service.store_resume_analysis(
            resume_filename="test_resume.pdf",
            job_description_filename="test_job.pdf", 
            analysis_results=test_data
        )
        print(f"✅ Test data stored successfully!")
        print(f"📄 Document ID: {document_id}")
        print(f"🎯 Data should now be visible in Firebase Console under 'results' collection")
        print("\nTo verify:")
        print("1. Open Firebase Console")
        print("2. Go to Firestore Database")
        print("3. Check the 'results' collection")
        print(f"4. Look for document with ID: {document_id}")
        
    except Exception as e:
        print(f"❌ Failed to store test data: {e}")

if __name__ == "__main__":
    main()