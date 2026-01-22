# How to Get Real Booking Confirmation Email

## ⚠️ Important: The Test Email is NOT a Booking Email

The email you received with subject "Booking Confirmation Test" is just a test email from the test script. It's NOT from an actual booking.

## ✅ To Get the REAL Booking Confirmation Email:

### You MUST Complete a Full Booking in the App:

1. **Open your Streamlit app** (http://localhost:8501 or your Streamlit Cloud URL)

2. **Start a booking** - Type in the chat:
   ```
   I want to make a booking
   ```
   or
   ```
   Book an appointment
   ```

3. **Answer ALL questions** the assistant asks:
   - Name: (e.g., "Spandana")
   - Email: (e.g., "spandana_doki@srmap.edu.in")
   - Phone: (e.g., "9346957877")
   - Booking type: (e.g., "consultation")
   - Date: (e.g., "2026-06-13")
   - Time: (e.g., "16:46")

4. **When you see the summary**, it will look like:
   ```
   Here are your booking details:
   
   Name: [your name]
   Email: [your email]
   Phone: [your phone]
   Booking type: [type]
   Date: [date]
   Time: [time]
   
   Please confirm: do you want me to place this booking? (yes/no)
   ```

5. **Type "yes"** to confirm

6. **Check your email** - You should receive:
   - Subject: "Booking Confirmation - ID: [number]"
   - Body with all your booking details

## 📧 What the Real Email Looks Like:

**Subject:** `Booking Confirmation - ID: 1`

**Body:**
```
Your booking has been confirmed!

Booking Details:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Booking ID: 1
Name: Spandana
Email: spandana_doki@srmap.edu.in
Phone: 9346957877
Service Type: consultation
Date: 2026-06-13
Time: 16:46
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Thank you for your booking!

If you need to make any changes, please contact us.
```

## 🔍 Troubleshooting:

### If you don't receive the email after confirming:

1. **Check the status messages** in the app (green boxes at the top):
   - Should show: "✅ Booking saved successfully!"
   - Should show: "📧 Confirmation email sent to [your email]"

2. **If you see an error message**, check:
   - Email configuration in secrets.toml
   - Check spam/junk folder

3. **Make sure you typed "yes"** to confirm the booking

## ❌ What You Received (Test Email):
- Subject: "Booking Confirmation Test" 
- Body: "Test booking email"
- This is NOT a real booking confirmation

## ✅ What You Should Receive (Real Booking):
- Subject: "Booking Confirmation - ID: [number]"
- Body: Full booking details with all information
- This comes ONLY after completing a booking in the app
