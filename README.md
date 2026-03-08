# Email Digest

Fetches Gmail, enriches with personal Notion context via RAG, and sends a tiered daily digest to Outlook.

## Pipeline
Gmail fetch → Notion RAG → LLM summarize → SMTP → Outlook

## Stack
Python, Anthropic API, Gmail API, Notion API, ChromaDB, GitHub Actions

## Setup
1. Copy `.env.example` to `.env` and fill in keys
2. Run Gmail OAuth: `python3 src/gmail_client.py`
3. Run: `python3 src/main.py`

## Required secrets (`.env`)
- `ANTHROPIC_API_KEY`
- `NOTION_API_KEY`
- `SMTP_SENDER`, `SMTP_PASSWORD`, `SMTP_RECIPIENT`
- `GMAIL_CREDENTIALS`, `GMAIL_TOKEN`
