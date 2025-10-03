#!/usr/bin/env python3
"""
Firebase Debug Test - Diagnose and fix Firebase credential issues
"""

import sys
import os
sys.path.append('src')

import json
from src.firebase.firebase_config import get_firebase_config, load_service_account_key, validate_firebase_config

def test_firebase_credentials():
    print("🔍 Firebase Credential Diagnostic")
    print("=" * 50)
    
    # Test 1: Configuration loading
    print("\n1. Testing configuration loading...")
    try:
        config = get_firebase_config()
        print(f"✅ Config loaded: {config['project_id']}")
        print(f"✅ Collection: {config['collection_name']}")
    except Exception as e:
        print(f"❌ Config loading failed: {e}")
        return False
    
    # Test 2: Service account file loading
    print("\n2. Testing service account file loading...")
    try:
        service_account = load_service_account_key()
        print(f"✅ Service account loaded")
        print(f"✅ Project ID: {service_account.get('project_id')}")
        print(f"✅ Client email: {service_account.get('client_email')}")
        
        # Check private key format
        private_key = service_account.get('private_key', '')
        if private_key.startswith('-----BEGIN PRIVATE KEY-----'):
            print("✅ Private key format looks correct")
        else:
            print("❌ Private key format issue")
            return False
            
    except Exception as e:
        print(f"❌ Service account loading failed: {e}")
        return False
    
    # Test 3: Firebase Admin SDK import
    print("\n3. Testing Firebase Admin SDK...")
    try:
        import firebase_admin
        from firebase_admin import credentials, firestore
        print("✅ Firebase Admin SDK imported successfully")
    except Exception as e:
        print(f"❌ Firebase Admin SDK import failed: {e}")
        return False
    
    # Test 4: Credential object creation
    print("\n4. Testing credential creation...")
    try:
        cred = credentials.Certificate(service_account)
        print("✅ Credential object created successfully")
    except Exception as e:
        print(f"❌ Credential creation failed: {e}")
        print(f"Error details: {str(e)}")
        return False
    
    # Test 5: Firebase initialization
    print("\n5. Testing Firebase initialization...")
    try:
        # Only initialize if not already done
        if not firebase_admin._apps:
            app = firebase_admin.initialize_app(cred, {
                'projectId': config['project_id']
            })
            print("✅ Firebase initialized successfully")
        else:
            print("✅ Firebase already initialized")
        
        # Test Firestore connection
        db = firestore.client()
        print("✅ Firestore client created")
        
    except Exception as e:
        print(f"❌ Firebase initialization failed: {e}")
        print(f"Error details: {str(e)}")
        return False
    
    print("\n🎉 All Firebase tests passed!")
    return True

if __name__ == "__main__":
    success = test_firebase_credentials()
    if success:
        print("\n✅ Firebase is ready to use!")
    else:
        print("\n❌ Firebase setup needs fixing")