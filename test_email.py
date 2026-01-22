"""
Quick test script to verify email configuration.
Run this to test if emails are working before testing in the app.
"""

import sys
sys.path.insert(0, '.')

try:
    import streamlit as st
    print("Testing with Streamlit secrets...")
    from tools import email_tool
    
    # Test email sending
    result = email_tool(
        to_email="spandana_doki@srmap.edu.in",
        subject="Test Email from Booking Assistant",
        body="This is a test email to verify your email configuration is working correctly."
    )
    
    if result.get("success"):
        print("[SUCCESS] Email sent successfully!")
        print(f"   Check your inbox: spandana_doki@srmap.edu.in")
        print(f"   Also check spam/junk folder")
    else:
        print("[FAILED] Email could not be sent")
        print(f"   Error: {result.get('error')}")
        print("\nTroubleshooting:")
        print("1. Check .streamlit/secrets.toml has correct values")
        print("2. Verify EMAIL_PASSWORD is a Gmail App Password (not regular password)")
        print("3. Make sure SMTP_SERVER = 'smtp.gmail.com'")
        print("4. For institutional emails, verify they use Gmail SMTP")
        
except Exception as e:
    print(f"[ERROR] {str(e)}")
    import traceback
    traceback.print_exc()
