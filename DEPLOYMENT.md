# 🚀 Resume Analyzer - Streamlit Deployment Guide

## Option 1: Streamlit Community Cloud (FREE)

### Prerequisites
- GitHub account with your code pushed
- OpenAI API key (for LLM features)

### Deployment Steps

1. **Visit Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account

2. **Deploy Your App**
   - Click "New app"
   - Repository: `PranavDoke/resume_analyzer_final`
   - Branch: `main`
   - Main file path: `web_app/app.py`
   - App URL: Choose your custom URL

3. **Configure Secrets**
   - In Streamlit Cloud, go to your app settings
   - Add secrets from `.streamlit/secrets.toml`:
   ```toml
   OPENAI_API_KEY = "your-actual-api-key"
   DATABASE_URL = "sqlite:///./resume_analyzer.db"
   ```

4. **Advanced Settings**
   - Python version: 3.9+
   - Requirements file: `requirements-deployment.txt`

### Post-Deployment Setup

1. **Download spaCy Model**
   - The app will automatically download required models on first run
   - May take 2-3 minutes for initial startup

2. **Test Features**
   - Single resume analysis
   - Batch analysis
   - Export functions

---

## Option 2: Local Production Deployment

### Using Docker (Recommended)

1. **Create Dockerfile**
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_sm

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "web_app/app.py", "--server.headless", "true", "--server.port", "8501"]
```

2. **Build and Run**
```bash
docker build -t resume-analyzer .
docker run -p 8501:8501 resume-analyzer
```

### Using Python Virtual Environment

1. **Setup Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

2. **Run Application**
```bash
streamlit run web_app/app.py --server.port 8501 --server.headless true
```

---

## Option 3: Cloud Platforms

### Heroku Deployment

1. **Create Procfile**
```
web: streamlit run web_app/app.py --server.port=$PORT --server.address=0.0.0.0
```

2. **Deploy**
```bash
heroku create your-app-name
git push heroku main
```

### AWS/GCP/Azure
- Use container services (ECS, Cloud Run, Container Instances)
- Follow Docker deployment method above

---

## Troubleshooting

### Common Issues
1. **Large file uploads** - Check maxUploadSize in config
2. **Memory issues** - Use lighter model versions
3. **Slow startup** - Pre-download models in container

### Performance Optimization
1. **Cache expensive operations**
2. **Use session state effectively**
3. **Optimize model loading**

### Monitoring
- Use Streamlit Cloud analytics
- Monitor memory and CPU usage
- Set up error tracking