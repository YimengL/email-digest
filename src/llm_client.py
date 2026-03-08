import anthropic
import os
from dotenv import load_dotenv


load_dotenv()
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


def summarize_emails(emails, context=""):
    email_text = ""
    for i, email in enumerate(emails, 1):
        email_text += f"\n--- Email {i} ---\n"
        email_text += f"From: {email['sender']}\n"
        email_text += f"Subject: {email['subject']}\n"
        email_text += f"Body: {email['body'][:600]}\n"
    
    context_section = f"\n\nPersonal context from my notes:\n{context}" if context else ""
    
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        system=f"""You are a personal email assistant.{context_section}
        Summarize the emails into 3 tiers:
        1. ACTION REQUIRED - needs a response or action
        2. IMPORTANT - good to know but no action needed
        3. EVERYTHING ELSE - low priority

        Return only the digest, no other text.""",
        messages=[
            {"role": "user", "content": f"Summarize these emails:\n{email_text}"}
        ]
    )
    
    return response.content[0].text


if __name__ == "__main__":

    from gmail_client import get_gmail_service, fetch_emails, parse_email
    service = get_gmail_service()
    raw_emails = fetch_emails(service)
    emails = [parse_email(r) for r in raw_emails]

    digest = summarize_emails(emails)
    print(digest)