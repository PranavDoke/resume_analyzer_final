"""
Test script to verify the full enterprise analyzer works
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_full_analyzer():
    """Test if full enterprise analyzer can be loaded and used"""
    try:
        print("🔄 Testing Full Enterprise Analyzer...")
        
        # Import the full analyzer
        from src.resume_analyzer import ResumeAnalyzer
        from config.settings import get_config
        
        print("✅ Successfully imported full enterprise analyzer")
        
        # Initialize with config
        config = get_config()
        analyzer = ResumeAnalyzer(config)
        
        print("✅ Full enterprise analyzer initialized successfully")
        print(f"📊 Analyzer type: Full Enterprise")
        
        return True
        
    except Exception as e:
        print(f"❌ Full enterprise analyzer test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_full_analyzer()
    if success:
        print("\n🎉 Full enterprise analyzer is ready!")
    else:
        print("\n💥 Full enterprise analyzer has issues")