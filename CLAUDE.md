# CLAUDE.md

# Email Digest Project

## Motivation
Gmail is blocked in China. Built this to automatically process personal emails
and forward a smart digest to Outlook — so I don't miss anything important while traveling.

## Project Goal
Learning project to understand LLM integration and RAG in practice.
Not production scale — personal use, daily batch job.

## Stack
- Python
- Anthropic API (Claude Haiku 4.5 for dev, Sonnet 4.5 for production)
- Gmail API
- Notion API
- GitHub Actions (scheduler)
- ChromaDB (vector store for RAG)
- SMTP (email delivery)

## Architecture
Gmail fetch → pre-filter → Notion RAG → LLM summarize → tiered digest → Outlook

## Key Design Decisions
- Pre-filter obvious non-important emails before LLM (cost + reliability)
- Notion page hierarchy used for retrieval weighting — subpages inherit parent importance
- High priority pages: interview-related, job search (hardcoded IDs in config)
- Tiered digest: ACTION REQUIRED / IMPORTANT / EVERYTHING ELSE
- Graceful degradation: if Notion fails, summarize without context; if LLM fails, send raw list
- Batch once daily — no real-time processing needed

## RAG Design
- Notion as personal knowledge base
- Retrieval grounds LLM summaries in personal context
- e.g. unknown sender + Notion says "applied to Sonar" = correctly flagged as important
- Hierarchy-based weighting: interview pages > travel pages > general notes

## Learning Approach
- Write ALL code myself — use Claude for explanation and guidance only, never generation
- Claude Code: ask for explanations, debugging help, code review only
- No exceptions — every line typed by me for full understanding

## Project Structure
```
email-digest/
  CLAUDE.md
  README.md
  .env                         ← never commit
  .gitignore
  requirements.txt
  phase0_warmup.py             ← throwaway API warmup, delete after Phase 0
  src/
    llm_client.py              ← LLM calls
    rag.py                     ← RAG pipeline
    notion_client.py           ← Notion retrieval
    gmail_client.py            ← Gmail fetch
    digest.py                  ← Digest formatting
    mailer.py                  ← SMTP delivery
    main.py                    ← Orchestration entry point
  .github/
    workflows/
      daily_digest.yml         ← GitHub Actions scheduler
```

## Sensitive Files — Never Commit
- `.env`
- `credentials.json`
- `token.json`