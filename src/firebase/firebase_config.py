"""
Firebase Configuration for Resume Analyzer
"""

import os
import json
from typing import Dict, Any

# Firebase Configuration
FIREBASE_CONFIG = {
    "project_id": os.getenv("FIREBASE_PROJECT_ID", "resumeanalyser-2cc38"),  # 👈 UPDATE THIS
    "collection_name": "results",  # 👈 Updated to match your Firebase console
    "service_account_path": os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH", "config/firebase_service_account.json"),
    "use_emulator": os.getenv("FIREBASE_USE_EMULATOR", "false").lower() == "true",
    "emulator_host": os.getenv("FIREBASE_EMULATOR_HOST", "localhost:8080")
}

# Service Account Configuration (for development - replace with actual credentials)
SAMPLE_SERVICE_ACCOUNT = {
    "type": "service_account",
    "project_id": "your-firebase-project-id",
    "private_key_id": "your-private-key-id",
    "private_key": "-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY_HERE\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-xxxxx@your-project.iam.gserviceaccount.com",
    "client_id": "your-client-id",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-xxxxx%40your-project.iam.gserviceaccount.com"
}

def get_firebase_config() -> Dict[str, Any]:
    """Get Firebase configuration"""
    return FIREBASE_CONFIG

def load_service_account_key() -> Dict[str, Any]:
    """
    Load Firebase service account key from file or environment variable
    
    Returns:
        Dict containing service account credentials
    """
    # Try to load from file first with multiple path options
    service_account_path = FIREBASE_CONFIG["service_account_path"]
    
    # Possible paths to check
    possible_paths = [
        service_account_path,  # Original path
        os.path.join(os.path.dirname(os.path.dirname(__file__)), service_account_path),  # From src/firebase to root
        os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), service_account_path),  # From web_app context
        os.path.abspath(service_account_path),  # Absolute path
        os.path.join(os.getcwd(), service_account_path)  # Current working directory
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r') as f:
                    credentials_data = json.load(f)
                    print(f"✅ Firebase credentials loaded from: {path}")
                    return credentials_data
            except Exception as e:
                print(f"⚠️ Failed to load credentials from {path}: {e}")
                continue
    
    # Try to load from environment variable
    service_account_json = os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON")
    if service_account_json:
        return json.loads(service_account_json)
    
    # Return sample configuration for development
    print("⚠️ Using sample Firebase configuration. Please update with your actual credentials.")
    return SAMPLE_SERVICE_ACCOUNT

def validate_firebase_config() -> bool:
    """
    Validate Firebase configuration
    
    Returns:
        bool: True if configuration is valid
    """
    try:
        config = get_firebase_config()
        service_account = load_service_account_key()
        
        # Check required fields
        required_fields = ["project_id", "collection_name"]
        for field in required_fields:
            if not config.get(field) or config[field] == "your-firebase-project-id":
                print(f"❌ Missing or invalid Firebase config: {field}")
                return False
        
        # Check service account
        required_sa_fields = ["type", "project_id", "private_key", "client_email"]
        for field in required_sa_fields:
            if not service_account.get(field) or "YOUR_" in str(service_account[field]):
                print(f"❌ Missing or invalid service account field: {field}")
                return False
        
        print("✅ Firebase configuration is valid")
        return True
    
    except Exception as e:
        print(f"❌ Firebase configuration validation failed: {e}")
        return False