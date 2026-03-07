import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_SENDER = os.environ.get("SMTP_SENDER")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")
SMTP_RECIPIENT = os.environ.get("SMTP_RECIPIENT")


def send_digest(subject, body):
    msg = MIMEMultipart()
    msg["From"] = SMTP_SENDER
    msg["To"] = SMTP_RECIPIENT
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_SENDER, SMTP_PASSWORD)
        server.sendmail(SMTP_SENDER, SMTP_RECIPIENT, msg.as_string())

if __name__ == "__main__":
    send_digest(
        subject="Daily Email Digest - Test",
        body="This is a test digest.\n\n1. ACTION REQUIRED\nNone\n\n2. IMPORTANT\nTest email received.\n\n3. EVERYTHING ELSE\nNone"
    )
    print("Sent!")