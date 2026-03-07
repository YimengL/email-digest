import os
from datetime import date
from dotenv import load_dotenv

load_dotenv()

from gmail_client import get_gmail_service, fetch_emails, parse_email
from llm_client import summarize_emails
from mailer import send_digest

def main():
    service = get_gmail_service()
    raw_emails = fetch_emails(service)
    emails = [parse_email(r) for r in raw_emails]

    if not emails:
        print("No emails found.")
        return
    
    digest = summarize_emails(emails)
    subject = f"Email Digest - {date.today()}"
    send_digest(subject, digest)
    print(f"Digest sent. {len(emails)} emails processed.")

if __name__ == "__main__":
    main()