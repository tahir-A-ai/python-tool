# Day 03: Mini AI Utilities

## Project Overview
**Goal:** To wrap AI logic into a professional **FastAPI** service with robustness and observability.
**Focus:** API development, retry logic, defensive JSON parsing, and separating business logic from the presentation layer.

## Tech Stack
* **Framework:** FastAPI + Uvicorn
* **AI Provider:** Google Gemini API (`gemini-2.5-flash`)
* **Utilities:** `tenacity` (conceptually), `logging`, `json`
* **Architecture:** Service Pattern (Logic vs. Interface)

## Key Features

### 1. Robust AI Service (`services.py`)
* **Retry Decorator:** A custom `@retry_with_backoff` wrapper that automatically retries failed API calls (handling 503 errors).
* **Defensive Parsing:** A hybrid parser that attempts `json.loads()` first, but falls back to manual text splitting if the AI ignores formatting rules.
* **Auto-Logging:** Every interaction is timestamped and saved to `api_logs.json` for debugging.

### 2. Dual Interfaces
* **Web API (`main.py`):** Exposes endpoints for `POST /extract-keywords` and `POST /summarize-bullets`.
* **CLI Tool (`sentiment_cli.py`):** A dedicated command-line tool for `Sentiment Analysis` with emoji-based feedback.

## Project Structure
```text
Week04_AI/Day03/
├── services.py       # The "Brain" (Shared Logic + Retry)
├── main.py           # FastAPI Server
├── sentiment_cli.py  # CLI Tool
├── api_logs.json     # Debug Logs
└── README.md         # Documentation

## How to Run

### 1. Start the API Server
This powers the Keyword Extractor and Bullet Point tools.
```bash
uvicorn main:app --reload
# Once running, documentation is available at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 2. Run the Sentiment Tool
```bash
python sentiment_cli.py

### Final Action
Run this to capture your new libraries (`fastapi`, `uvicorn`) in the root file:
```powershell
pip freeze > ../requirements.txt
