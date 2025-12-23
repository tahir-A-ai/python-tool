# Day 02: Working with LLMs APIs (Gemini API)

## Project Overview
**Goal:** Integrating Large Language Models (LLMs) into Python scripts.
**Focus:** API authentication, modular software architecture, prompt engineering strategies, and observability (logging).

This module treats Intelligence as a Service (IaaS), building reusable tools for text summarization, style rewriting, and sentiment classification using Google's Gemini 2.5 Flash.

## Tech Stack
* **Language:** Python 3.x
* **AI Provider:** Google Gemini API (`gemini-2.5-flash`)
* **SDK:** `google-generativeai`
* **Security:** `python-dotenv` (Environment Variable Management)
* **Architecture:** Modular Driver/Engine Pattern

## Key Achievements

### 1. Secure API Integration
* Configured a secure authentication pipeline using a root-level `.env` file.
* Implemented the **"Single Source of Truth"** principle for API keys, allowing multiple daily folders to share credentials safely.

### 2. Modular Architecture (The Engine Pattern)
Refactored monolithic code into a professional structure:
* **`utils.py` (The Engine):** Handles API connection, error handling, and JSON logging.
* **Driver Scripts:** Separate CLI tools for specific tasks, adhering to the *Single Responsibility Principle (SRP)*.

### 3. Prompt Engineering Tools
Built three distinct CLI tools to demonstrate core AI capabilities:
* **`summarize_txt.py`:** Uses **Constraint Prompting** to compress text into single-sentence outputs.
* **`rewrite_txt.py`:** Uses **Persona/Audience Injection** to dynamically change the tone of text (e.g., "Explain to a 5-year-old").
* **`classify_txt.py`:** Uses **System Directives** to force strict categorical outputs (POSITIVE/NEGATIVE/URGENT) suitable for backend logic.

### 4. Observability & Debugging
* Implemented an automatic **JSON Logger** (`prompt_logs.json`).
* Records every prompt sent and response received, creating a "Black Box" for debugging non-deterministic AI behavior.

## Project Structure
```text
Week04_AI/
├── .env                    # Shared API Credentials (Hidden)
├── Day02/
│   ├── utils.py            # Core Logic (API & Logging)
│   ├── summarize_txt.py    # CLI Tool: Summarization
│   ├── rewrite_txt.py      # CLI Tool: Style Transfer
│   ├── classify_txt.py     # CLI Tool: Sentiment Analysis
│   ├── prompt_logs.json    # Auto-generated Debug Logs
│   └── README.md           # Documentation
└── requirements.txt        # Dependencies