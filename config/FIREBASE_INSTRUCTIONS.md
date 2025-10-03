# Firebase Configuration Instructions

## Step 4A: Place Service Account File

1. Rename your downloaded service account JSON file to: `firebase_service_account.json`
2. Place it in the config directory:

```
resume_analyzer_final/
├── config/
│   ├── firebase_service_account.json  ← Place your file here
│   ├── settings.py
│   └── __init__.py
```

## Step 4B: Update Project Configuration

Edit the firebase configuration file with your actual project ID.