#!/bin/bash
# Install system dependencies
apt-get update && apt-get install -y build-essential

# Install Python dependencies
pip install -r requirements-deployment.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Start the application
streamlit run web_app/app.py --server.port=$PORT --server.address=0.0.0.0