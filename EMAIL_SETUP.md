# Email Configuration Guide

## Issue: Not Receiving Emails After Booking Confirmation

The email functionality has been fixed to read from Streamlit secrets. Here's what you need to know:

## For Gmail Users

### Important: Use App Password, Not Regular Password

Gmail requires an **App Password** for SMTP authentication, not your regular Gmail password.

### Steps to Get Gmail App Password:

1. **Enable 2-Step Verification** (if not already enabled):
   - Go to your Google Account: https://myaccount.google.com/
   - Click "Security" → "2-Step Verification"
   - Follow the prompts to enable it

2. **Generate App Password**:
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" as the app
   - Select "Other (Custom name)" as the device
   - Enter "Streamlit Booking Assistant" as the name
   - Click "Generate"
   - Copy the 16-character password (it will look like: `abcd efgh ijkl mnop`)

3. **Update Your Secrets**:
   - In `.streamlit/secrets.toml` (for local testing)
   - In Streamlit Cloud → Settings → Secrets (for deployment)
   
   Set:
   ```toml
   EMAIL_USER = "your_email@gmail.com"
   EMAIL_PASSWORD = "your_16_char_app_password"  # Use the app password, not your regular password
   SMTP_SERVER = "smtp.gmail.com"
   SMTP_PORT = "587"
   ```

## For Other Email Providers

### Outlook/Hotmail:
```toml
SMTP_SERVER = "smtp-mail.outlook.com"
SMTP_PORT = "587"
```

### Yahoo:
```toml
SMTP_SERVER = "smtp.mail.yahoo.com"
SMTP_PORT = "587"
```

### Custom SMTP:
```toml
SMTP_SERVER = "smtp.yourprovider.com"
SMTP_PORT = "587"  # or "465" for SSL
```

## Testing Email Functionality

After updating your secrets:

1. **Restart your Streamlit app** (if running locally)
2. **Create a test booking**
3. **Check the status messages** - you should see:
   - "Booking saved to database (booking_id=X)"
   - "Confirmation email sent." (if successful)
   - OR "Booking saved, but email failed: [error message]" (if there's an issue)

## Common Issues

### Issue: "SMTP configuration missing"
- **Solution**: Make sure all email secrets are set in `.streamlit/secrets.toml` or Streamlit Cloud secrets

### Issue: "Authentication failed"
- **Solution**: 
  - For Gmail: Make sure you're using an App Password, not your regular password
  - Check that 2-Step Verification is enabled
  - Verify the email and password are correct

### Issue: "Connection timeout"
- **Solution**: 
  - Check your firewall settings
  - Verify SMTP_SERVER and SMTP_PORT are correct for your provider
  - Some networks block SMTP ports - try a different network

### Issue: Emails going to spam
- **Solution**: 
  - Check spam/junk folder
  - The "From" address will be your EMAIL_USER address
  - Consider using a dedicated email address for sending

## Verification Checklist

- [ ] 2-Step Verification enabled (for Gmail)
- [ ] App Password generated and copied
- [ ] EMAIL_USER set to your email address
- [ ] EMAIL_PASSWORD set to your App Password (16 characters, no spaces)
- [ ] SMTP_SERVER set correctly (smtp.gmail.com for Gmail)
- [ ] SMTP_PORT set to "587"
- [ ] Secrets updated in both local `.streamlit/secrets.toml` AND Streamlit Cloud
- [ ] App restarted after updating secrets

## Security Note

⚠️ **Never commit real passwords to Git!**

- The `secrets.toml` file should be in `.gitignore`
- Use placeholder values in your repository
- Only set real values in:
  - Local `.streamlit/secrets.toml` (for local testing)
  - Streamlit Cloud Secrets (for deployment)
