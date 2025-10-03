"""
Firebase Service Module for Resume Analyzer
Handles all Firebase Firestore operations for storing resume analysis results
"""

import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List
import json
import os
import traceback
import uuid

from .firebase_config import get_firebase_config, load_service_account_key, validate_firebase_config


class FirebaseService:
    """
    Firebase service for handling resume analysis data storage
    """
    
    def __init__(self):
        """Initialize Firebase service"""
        self.db = None
        self.collection_name = "results"  # Default to results collection
        self.initialized = False
        
        try:
            self._initialize_firebase()
        except Exception as e:
            print(f"⚠️ Firebase initialization failed: {e}")
            print("Resume analysis will continue without Firebase logging.")
    
    def _initialize_firebase(self):
        """Initialize Firebase Admin SDK"""
        try:
            # Check if Firebase is already initialized
            if not firebase_admin._apps:
                # Load configuration
                config = get_firebase_config()
                service_account = load_service_account_key()
                
                # Initialize Firebase Admin SDK with error handling
                try:
                    cred = credentials.Certificate(service_account)
                    firebase_admin.initialize_app(cred, {
                        'projectId': config['project_id']
                    })
                    print("✅ Firebase Admin SDK initialized")
                except Exception as cred_error:
                    print(f"❌ Firebase credential error: {cred_error}")
                    # Try to reinitialize Firebase if there's a credential issue
                    for app in firebase_admin._apps.copy():
                        firebase_admin.delete_app(firebase_admin._apps[app])
                    raise cred_error
            
            # Get Firestore client
            self.db = firestore.client()
            
            # Get collection name from config
            config = get_firebase_config()
            self.collection_name = config.get('collection_name', 'results')
            self.initialized = True
            
            print(f"✅ Firebase service initialized successfully - Collection: {self.collection_name}")
            
        except Exception as e:
            print(f"❌ Firebase initialization error: {e}")
            self.initialized = False
            raise
    
    def is_initialized(self) -> bool:
        """Check if Firebase service is properly initialized"""
        return self.initialized and self.db is not None
    
    def store_resume_analysis(self, 
                            resume_filename: str,
                            job_description_filename: str,
                            analysis_results: Dict[str, Any],
                            user_info: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """
        Store resume analysis results in Firebase Firestore
        
        Args:
            resume_filename: Name of the resume file
            job_description_filename: Name of the job description file
            analysis_results: Complete analysis results with all scoring parameters
            user_info: Optional user information (IP, session, etc.)
        
        Returns:
            str: Document ID if successful, None if failed
        """
        if not self.is_initialized():
            print("⚠️ Firebase not initialized, skipping data storage")
            return None
        
        try:
            # Generate unique document ID
            doc_id = str(uuid.uuid4())
            
            # Prepare document data
            document_data = self._prepare_document_data(
                resume_filename, 
                job_description_filename, 
                analysis_results, 
                user_info
            )
            
            # Store in Firestore
            doc_ref = self.db.collection(self.collection_name).document(doc_id)
            doc_ref.set(document_data)
            
            print(f"✅ Resume analysis stored in Firebase with ID: {doc_id}")
            return doc_id
            
        except Exception as e:
            print(f"❌ Error storing resume analysis in Firebase: {e}")
            print(f"Error details: {traceback.format_exc()}")
            return None
    
    def _prepare_document_data(self, 
                              resume_filename: str,
                              job_description_filename: str,
                              analysis_results: Dict[str, Any],
                              user_info: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Prepare document data for Firebase storage
        
        Args:
            resume_filename: Name of the resume file
            job_description_filename: Name of the job description file
            analysis_results: Complete analysis results
            user_info: Optional user information
        
        Returns:
            Dict: Formatted document data for Firebase
        """
        timestamp = datetime.now(timezone.utc)
        
        # Extract scoring details from analysis results
        scoring_details = self._extract_scoring_details(analysis_results)
        
        document_data = {
            # Metadata
            "timestamp": timestamp,
            "resume_filename": resume_filename,
            "job_description_filename": job_description_filename,
            
            # Overall Scores
            "overall_score": analysis_results.get('analysis_results', {}).get('overall_score', 0),
            "match_level": analysis_results.get('analysis_results', {}).get('match_level', 'Unknown'),
            
            # Detailed Scoring Parameters
            "scoring_details": scoring_details,
            
            # Component Scores
            "hard_matching": {
                "score": analysis_results.get('analysis_results', {}).get('hard_matching', {}).get('score', 0),
                "weight": analysis_results.get('analysis_results', {}).get('hard_matching', {}).get('weight', 0),
                "weighted_score": analysis_results.get('analysis_results', {}).get('hard_matching', {}).get('weighted_score', 0),
                "details": analysis_results.get('analysis_results', {}).get('hard_matching', {}).get('details', {})
            },
            
            "soft_matching": {
                "score": analysis_results.get('analysis_results', {}).get('soft_matching', {}).get('score', 0),
                "weight": analysis_results.get('analysis_results', {}).get('soft_matching', {}).get('weight', 0),
                "weighted_score": analysis_results.get('analysis_results', {}).get('soft_matching', {}).get('weighted_score', 0),
                "details": analysis_results.get('analysis_results', {}).get('soft_matching', {}).get('details', {})
            },
            
            "llm_analysis": {
                "score": analysis_results.get('analysis_results', {}).get('llm_analysis', {}).get('score', 0),
                "weight": analysis_results.get('analysis_results', {}).get('llm_analysis', {}).get('weight', 0),
                "weighted_score": analysis_results.get('analysis_results', {}).get('llm_analysis', {}).get('weighted_score', 0),
                "reasoning": analysis_results.get('analysis_results', {}).get('llm_analysis', {}).get('reasoning', ''),
                "confidence": analysis_results.get('analysis_results', {}).get('llm_analysis', {}).get('confidence', 0)
            },
            
            # Hiring Recommendation
            "hiring_recommendation": analysis_results.get('hiring_recommendation', {}),
            
            # Gap Analysis
            "gap_analysis": analysis_results.get('gap_analysis', {}),
            
            # Extracted Information
            "extracted_info": {
                "resume_skills": analysis_results.get('extracted_info', {}).get('resume_skills', []),
                "resume_keywords": analysis_results.get('extracted_info', {}).get('resume_keywords', []),
                "jd_requirements": analysis_results.get('extracted_info', {}).get('jd_requirements', []),
                "jd_skills": analysis_results.get('extracted_info', {}).get('jd_skills', [])
            },
            
            # User Information (if provided)
            "user_info": user_info or {},
            
            # Processing Information
            "processing_info": {
                "processing_time": analysis_results.get('processing_time', 0),
                "model_versions": analysis_results.get('model_versions', {}),
                "system_info": analysis_results.get('system_info', {})
            }
        }
        
        return document_data
    
    def _extract_scoring_details(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract detailed scoring parameters from analysis results
        
        Args:
            analysis_results: Complete analysis results
        
        Returns:
            Dict: Detailed scoring breakdown
        """
        try:
            analysis_data = analysis_results.get('analysis_results', {})
            
            scoring_details = {
                # Skills matching
                "skills_match_score": analysis_data.get('hard_matching', {}).get('details', {}).get('skills_match_score', 0),
                "skills_found": analysis_data.get('hard_matching', {}).get('details', {}).get('skills_found', []),
                "skills_missing": analysis_data.get('hard_matching', {}).get('details', {}).get('skills_missing', []),
                
                # Keywords matching
                "keyword_match_score": analysis_data.get('hard_matching', {}).get('details', {}).get('keyword_match_score', 0),
                "keywords_found": analysis_data.get('hard_matching', {}).get('details', {}).get('keywords_found', []),
                "keywords_missing": analysis_data.get('hard_matching', {}).get('details', {}).get('keywords_missing', []),
                
                # Experience matching
                "experience_match": analysis_data.get('hard_matching', {}).get('details', {}).get('experience_match', 0),
                "education_match": analysis_data.get('hard_matching', {}).get('details', {}).get('education_match', 0),
                
                # TF-IDF and BM25 scores
                "tfidf_score": analysis_data.get('hard_matching', {}).get('details', {}).get('tfidf_score', 0),
                "bm25_score": analysis_data.get('hard_matching', {}).get('details', {}).get('bm25_score', 0),
                
                # Semantic similarity
                "semantic_similarity": analysis_data.get('soft_matching', {}).get('details', {}).get('semantic_similarity', 0),
                "embedding_similarity": analysis_data.get('soft_matching', {}).get('details', {}).get('embedding_similarity', 0),
                
                # Context understanding
                "context_relevance": analysis_data.get('soft_matching', {}).get('details', {}).get('context_relevance', 0),
                "role_alignment": analysis_data.get('soft_matching', {}).get('details', {}).get('role_alignment', 0),
                
                # LLM specific scores
                "llm_reasoning_score": analysis_data.get('llm_analysis', {}).get('score', 0),
                "llm_confidence": analysis_data.get('llm_analysis', {}).get('confidence', 0),
                "llm_verdict": analysis_data.get('llm_analysis', {}).get('verdict', ''),
                
                # Overall calculations
                "total_weighted_score": analysis_data.get('overall_score', 0),
                "match_percentage": analysis_data.get('overall_score', 0)
            }
            
            return scoring_details
            
        except Exception as e:
            print(f"⚠️ Error extracting scoring details: {e}")
            return {}
    
    def get_analysis_history(self, 
                           limit: int = 100,
                           start_date: Optional[datetime] = None,
                           end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """
        Retrieve analysis history from Firebase
        
        Args:
            limit: Maximum number of records to retrieve
            start_date: Start date for filtering
            end_date: End date for filtering
        
        Returns:
            List of analysis records
        """
        if not self.is_initialized():
            print("⚠️ Firebase not initialized")
            return []
        
        try:
            query = self.db.collection(self.collection_name).order_by('timestamp', direction=firestore.Query.DESCENDING)
            
            # Apply date filters if provided
            if start_date:
                query = query.where('timestamp', '>=', start_date)
            if end_date:
                query = query.where('timestamp', '<=', end_date)
            
            # Apply limit
            query = query.limit(limit)
            
            # Execute query
            docs = query.stream()
            
            results = []
            for doc in docs:
                data = doc.to_dict()
                data['id'] = doc.id
                results.append(data)
            
            print(f"✅ Retrieved {len(results)} analysis records from Firebase")
            return results
            
        except Exception as e:
            print(f"❌ Error retrieving analysis history: {e}")
            return []
    
    def get_analytics_summary(self) -> Dict[str, Any]:
        """
        Get analytics summary from stored data
        
        Returns:
            Dict: Analytics summary
        """
        if not self.is_initialized():
            return {}
        
        try:
            # Get recent analyses (last 1000)
            analyses = self.get_analysis_history(limit=1000)
            
            if not analyses:
                return {"message": "No data available"}
            
            # Calculate summary statistics
            total_analyses = len(analyses)
            avg_score = sum(a.get('overall_score', 0) for a in analyses) / total_analyses if total_analyses > 0 else 0
            
            # Score distribution
            excellent = sum(1 for a in analyses if a.get('overall_score', 0) >= 80)
            good = sum(1 for a in analyses if 65 <= a.get('overall_score', 0) < 80)
            fair = sum(1 for a in analyses if 45 <= a.get('overall_score', 0) < 65)
            poor = sum(1 for a in analyses if a.get('overall_score', 0) < 45)
            
            summary = {
                "total_analyses": total_analyses,
                "average_score": round(avg_score, 2),
                "score_distribution": {
                    "excellent": excellent,
                    "good": good,
                    "fair": fair,
                    "poor": poor
                },
                "date_range": {
                    "latest": analyses[0].get('timestamp') if analyses else None,
                    "oldest": analyses[-1].get('timestamp') if analyses else None
                }
            }
            
            return summary
            
        except Exception as e:
            print(f"❌ Error generating analytics summary: {e}")
            return {"error": str(e)}


# Global Firebase service instance
firebase_service = FirebaseService()


def get_firebase_service() -> FirebaseService:
    """Get the global Firebase service instance"""
    return firebase_service