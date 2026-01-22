# Streamlit Cloud Deployment Guide

## Issue: Health Check Failing

If you're seeing the error:
```
The service has encountered an error while checking the health of the Streamlit app: Get "http://localhost:8501/healthz": dial tcp 127.0.0.1:8501: connect: connection refused
```

This means Streamlit is not starting properly. Follow these steps:

## Step 1: Configure Secrets in Streamlit Cloud

1. Go to your Streamlit Cloud app settings
2. Click on "Secrets" in the left sidebar
3. Add the following secrets in TOML format:

```toml
GEMINI_API_KEY = "your_actual_gemini_api_key_here"

EMAIL_USER = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password_here"

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = "587"
```

**Important:** 
- Replace all placeholder values with your actual credentials
- For Gmail, you need to use an "App Password", not your regular password
- The GEMINI_API_KEY is required for the app to function

## Step 2: Verify Main File Path

In Streamlit Cloud settings, ensure:
- **Main file path:** `main.py` (not `app/main.py`)

## Step 3: Check Repository Structure

Your repository should have:
- `main.py` (entry point)
- `requirements.txt`
- `.streamlit/config.toml` (optional, but recommended)
- All Python modules in the root directory

## Step 4: Common Issues

### Issue: App crashes on startup
- **Solution:** Make sure all secrets are configured in Streamlit Cloud
- Check the logs for specific error messages

### Issue: Import errors
- **Solution:** Ensure all files are in the root directory (not in `app/` subdirectory)
- All imports should be relative (e.g., `from chat_logic import ...`)

### Issue: Database errors
- **Solution:** The database will be created automatically on first run
- SQLite files are ephemeral on Streamlit Cloud (they reset on redeploy)

## Step 5: Test Locally First

Before deploying, test locally:
```bash
streamlit run main.py
```

If it works locally, it should work on Streamlit Cloud (assuming secrets are configured).

## Step 6: View Logs

In Streamlit Cloud:
1. Go to your app
2. Click on "Manage app"
3. Click on "Logs" to see detailed error messages
4. Look for Python tracebacks or import errors

## Quick Fix Checklist

- [ ] All secrets configured in Streamlit Cloud
- [ ] Main file path is `main.py`
- [ ] `requirements.txt` is present and up to date
- [ ] All Python files are in root directory
- [ ] No syntax errors (test locally first)
- [ ] GEMINI_API_KEY is valid and active
