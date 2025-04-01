# Knowledge Explorer

> Discover and explore any topic — curiosity is your compass.

**Knowledge Explorer** is a web-based application built with **React, Python, Flask, PostgreSQL, and Redis**, designed to help users learn about any topic at their preferred comprehension level. The app retrieves content and internal links from Wikipedia and leverages a language model (LLM) to generate summaries at three depths: **basic**, **intermediate**, and **advanced**.

Its ultimate goal is to construct a dynamic, AI-assisted learning path tailored to each user's curiosity.

---

## Features

- **Dynamic Topic Search** — Users enter a topic to fetch related Wikipedia content.
- **Content Extraction** — Retrieves both page text and internal links for deeper exploration.
- **LLM Summarization** — Uses a cost-efficient LLM to generate multi-level summaries (basic → advanced).
- **Learning Path Generation** — Organizes related topics into a coherent, structured learning experience.
- **Caching & Storage** — Utilizes both Redis and browser caching to minimize API calls and store generated content.
- **Database Integration** — Summaries, Learning paths, User input redirects, are stored in PostgreSQL or SQLite (local dev).

---

## Tech Stack

**Frontend**:  
- React

**Backend**:  
- Python  
- Flask  
- Flask-Migrate, SQLAlchemy

**Database**:  
- PostgreSQL (production)  
- SQLite (for local development)

**Caching**:  
- Redis (via Flask-Caching)  
- Browser local/session storage

**APIs**:  
- Wikipedia (MediaWiki API)  
- Anthropic Claude (LLM)

**Deployment**:  
- Docker (containers for frontend/backend)  
- AWS EC2 (app hosting), RDS (PostgreSQL), ElastiCache (Redis)

**Version Control**:  
- Git + GitHub
