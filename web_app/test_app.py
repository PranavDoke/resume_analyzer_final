"""
Simple test version of the Streamlit app
"""

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Resume Analyzer - Test",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Simple test
def main():
    st.title("🎯 Resume Analyzer - Test")
    st.write("This is a test to verify Streamlit is working correctly.")
    
    st.sidebar.title("Navigation Test")
    page = st.sidebar.selectbox("Choose page:", ["Home", "Test"])
    
    if page == "Home":
        st.write("Welcome to the home page!")
        st.success("App is working correctly!")
    else:
        st.write("This is the test page!")
        st.info("Navigation is working!")

if __name__ == "__main__":
    main()