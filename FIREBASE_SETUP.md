# Firebase Integration Setup Guide

## Overview
This guide will help you set up Firebase integration with your Resume Analyzer project. Once configured, every resume analysis will automatically log detailed scoring results to your Firebase Firestore database in the `resumeanalyser` collection.

## What Gets Logged
Every time someone uses the system to analyze a resume, the following data is stored in Firebase:

### Core Information
- Timestamp of analysis
- Resume filename and Job Description filename
- Overall relevance score (0-100)
- Match level (Excellent/Good/Fair/Poor)

### Detailed Scoring Parameters
- **Skills Matching**: Individual skill scores, found/missing skills
- **Keyword Matching**: Keyword relevance scores, found/missing keywords
- **Experience Matching**: Experience and education alignment scores
- **TF-IDF/BM25 Scores**: Text similarity metrics
- **Semantic Similarity**: AI-powered semantic matching scores
- **LLM Analysis**: AI reasoning, confidence, and verdict
- **Hiring Recommendation**: Final decision with confidence level

### Component Breakdown
- Hard Matching (40% weight): Skills, keywords, TF-IDF, BM25
- Soft Matching (30% weight): Semantic similarity, context relevance
- LLM Analysis (30% weight): AI reasoning and gap analysis

## Setup Steps

### Step 1: Create Firebase Project
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Create a project" or "Add project"
3. Enter your project name (e.g., "resume-analyzer-analytics")
4. Enable Google Analytics if desired
5. Click "Create project"

### Step 2: Enable Firestore Database
1. In your Firebase project, go to "Build" → "Firestore Database"
2. Click "Create database"
3. Choose "Start in test mode" for development (or "production mode" for production)
4. Select a location for your database
5. Click "Done"

### Step 3: Create Service Account
1. Go to "Project Settings" (gear icon) → "Service accounts"
2. Click "Generate new private key"
3. Click "Generate key" - this will download a JSON file
4. Save this file securely (it contains sensitive credentials)

### Step 4: Configure Your Project

#### Option A: Using JSON File (Recommended)
1. Rename your downloaded service account file to `firebase_service_account.json`
2. Place it in the `config/` directory of your project:
   ```
   resume_analyzer_final/
   ├── config/
   │   └── firebase_service_account.json  ← Place here
   ```

#### Option B: Using Environment Variables
Set the following environment variables:
```bash
export FIREBASE_PROJECT_ID="your-project-id"
export FIREBASE_SERVICE_ACCOUNT_JSON='{"type":"service_account","project_id":"..."}' 
```

### Step 5: Update Configuration
Edit `src/firebase/firebase_config.py` and update:
```python
FIREBASE_CONFIG = {
    "project_id": "your-actual-firebase-project-id",  # Update this
    "collection_name": "resumeanalyser",
    # ... rest stays the same
}
```

### Step 6: Test Integration
Run the test script to verify everything works:
```bash
python test_firebase_integration.py
```

You should see:
- ✅ Firebase Admin SDK: Installed
- ✅ Configuration: Valid
- ✅ Service: Ready
- ✅ Integration: Complete

## Firestore Data Structure

Each resume analysis creates a document in the `resumeanalyser` collection with this structure:

```json
{
  "timestamp": "2024-01-01T00:00:00Z",
  "resume_filename": "john_doe_resume.pdf",
  "job_description_filename": "senior_developer_jd.pdf",
  "overall_score": 85.5,
  "match_level": "excellent",
  
  "scoring_details": {
    "skills_match_score": 85.0,
    "skills_found": ["Python", "React", "AWS"],
    "skills_missing": ["Docker", "Kubernetes"],
    "keyword_match_score": 78.0,
    "semantic_similarity": 90.0,
    "llm_reasoning_score": 88.0,
    "total_weighted_score": 85.5
  },
  
  "hard_matching": {
    "score": 80.0,
    "weight": 0.4,
    "weighted_score": 32.0,
    "details": { /* detailed breakdown */ }
  },
  
  "soft_matching": {
    "score": 88.0,
    "weight": 0.3,
    "weighted_score": 26.4,
    "details": { /* semantic analysis */ }
  },
  
  "llm_analysis": {
    "score": 90.0,
    "weight": 0.3,
    "weighted_score": 27.0,
    "reasoning": "Strong technical background...",
    "confidence": 95.0,
    "verdict": "HIRE"
  },
  
  "hiring_recommendation": {
    "decision": "HIRE",
    "confidence": 92.0,
    "reasoning": "Excellent match for the role"
  },
  
  "extracted_info": {
    "resume_skills": ["Python", "React", "AWS", "SQL"],
    "jd_requirements": ["3+ years", "Python", "Cloud"]
  },
  
  "user_info": {
    "session_id": "abc-123-def",
    "ip_address": "192.168.1.100",
    "timestamp": 1609459200
  }
}
```

## Security Configuration

### Production Setup
For production, configure Firestore security rules:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /resumeanalyser/{document} {
      // Only allow server-side writes
      allow read, write: if false;
    }
  }
}
```

### Environment Variables (Production)
```bash
FIREBASE_PROJECT_ID=your-production-project-id
FIREBASE_SERVICE_ACCOUNT_JSON={"type":"service_account",...}
```

## Usage Analytics

You can query your data to get insights:

### Basic Queries
```javascript
// Get all analyses from last 7 days
db.collection('resumeanalyser')
  .where('timestamp', '>', new Date(Date.now() - 7*24*60*60*1000))
  .orderBy('timestamp', 'desc')

// Get high-scoring candidates
db.collection('resumeanalyser')
  .where('overall_score', '>=', 80)
  .orderBy('overall_score', 'desc')

// Get analyses by job posting
db.collection('resumeanalyser')
  .where('job_description_filename', '==', 'senior_developer_jd.pdf')
```

### Analytics Dashboard
You can build dashboards to track:
- Average scores over time
- Most common missing skills
- Hiring decision distribution
- Processing performance metrics

## Troubleshooting

### Common Issues

**1. "Import firebase_admin could not be resolved"**
```bash
pip install firebase-admin
```

**2. "Failed to initialize certificate credential"**
- Check that your service account JSON is valid
- Ensure the file path is correct
- Verify the private key format

**3. "Permission denied"**
- Check Firestore security rules
- Verify service account has Firestore write permissions

**4. "Project not found"**
- Ensure project_id in config matches your Firebase project
- Check that Firestore is enabled in your project

### Debugging
Enable debug logging:
```python
import logging
logging.getLogger('firebase_admin').setLevel(logging.DEBUG)
```

## Cost Considerations

Firestore pricing (as of 2024):
- Document reads: $0.06 per 100,000
- Document writes: $0.18 per 100,000  
- Document deletes: $0.02 per 100,000
- Storage: $0.18 per GiB/month

For a typical resume analysis system:
- ~1KB per analysis document
- 1000 analyses/month = $0.002 in writes + minimal storage
- Very cost-effective for most use cases

## Data Privacy

**Important**: Resume analysis data may contain sensitive information. Consider:
1. Implementing data retention policies
2. Anonymizing personal information
3. Complying with GDPR/privacy regulations
4. Regular data audits

## Support

If you encounter issues:
1. Check the console logs for error messages
2. Run `python test_firebase_integration.py` to diagnose
3. Verify your Firebase project settings
4. Check Firestore security rules

The integration is designed to fail gracefully - if Firebase is unavailable, the resume analysis will continue normally without logging.