# Web Scraping & API Pipeline Context

## 🧭 Domain Context
This pipeline manages web crawling, HTTP client tools, and structured data extraction from remote APIs.

## ⚖️ Component Rules
- **Respect API Limits**: Scraping tools MUST respect rate limits and include logical retries with exponential backoff.
- **Resilience**: Network calls should be routed through the Self-Healing Environment policies for stability.
