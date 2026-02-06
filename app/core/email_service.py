import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv
load_dotenv()

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

def send_alert_email(service: str, message: str):
    msg = EmailMessage()
    msg["Subject"] = f"CRITICAL ALERT from {service}"
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER

    msg.set_content(
        f"""
CRITICAL ALERT DETECTED

Service: {service}
Message: {message}

Immediate attention required.
"""
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)
