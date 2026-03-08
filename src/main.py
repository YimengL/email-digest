import os
from datetime import date
from dotenv import load_dotenv

load_dotenv()

from gmail_client import get_gmail_service, fetch_emails, parse_email
from llm_client import summarize_emails
from mailer import send_digest
from notion_fetcher import fetch_pages, fetch_page_content
from rag import build_index, retrieve_context


def main():
    # Build Notion index
    pages = fetch_pages()
    for page in pages:
        page["content"] = fetch_page_content(page["id"])
    build_index(pages)

    # Fetch emails
    service = get_gmail_service()
    raw_emails = fetch_emails(service)
    emails = [parse_email(r) for r in raw_emails]

    if not emails:
        print("No emails found.")
        return

    # Retrieve context and summarize
    query = " ".join([e["subject"] + " " + e["sender"] for e in emails])
    context = retrieve_context(query)

    digest = summarize_emails(emails, context=context)
    subject = f"Email Digest - {date.today()}"
    send_digest(subject, digest)
    print(f"Digest sent. {len(emails)} emails processed.")

if __name__ == "__main__":
    main()