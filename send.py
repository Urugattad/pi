import smtplib
from email.message import EmailMessage

# Email Configuration
SMTP_SERVER = "smtp.gmail.com"  # Use your email provider's SMTP server
SMTP_PORT = 587  # TLS Port
EMAIL_SENDER = "gurudatta220928@gmail.com"
EMAIL_PASSWORD = "lapg qrkm pdvd hthg"  # ⚠️ Use an App Password, NOT your real password!
EMAIL_RECEIVER = "gpaykaru@gmail.com"

def send_email_alert():
    msg = EmailMessage()
    msg["Subject"] = "Motion Detected Alert!"
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg.set_content("Warning: Motion detected on your Raspberry Pi!")

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Secure the connection
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")


motion_detected = True
if motion_detected:
     send_email_alert()  # Send email if motion is detected
	
    
