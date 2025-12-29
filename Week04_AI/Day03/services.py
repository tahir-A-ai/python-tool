import os
import time
import json
import logging
import google.generativeai as genai
from dotenv import load_dotenv
from functools import wraps
import datetime

# 1. Setup Logging
# to see logs in the console to know what's happening
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 2. Load Env & Configure Gemini
load_dotenv(dotenv_path='../.env')
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("API Key missing!")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')
LOG_FILE = "api_logs.json"


# --- HELPER: Save to JSON File ---
def log_interaction(task_type, input_text, output_data):
    """Saves the interaction to a JSON log file."""
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "task": task_type,
        "input_snippet": input_text[:50] + "..." if len(input_text) > 50 else input_text,
        "output": output_data
    }
    
    # Read existing logs or start new
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, 'r') as f:
                logs = json.load(f)
        except (json.JSONDecodeError, ValueError):
            logs = []
    else:
        logs = []
        
    logs.append(entry)
    
    with open(LOG_FILE, 'w') as f:
        json.dump(logs, f, indent=4)


# Retry-Logic >> created decorator so that we can call it on top of every ednpoint.
def retry_with_backoff(retries=3, delay=2):
    """
    A decorator that retries a function if it fails.
    retries: Max attempts
    delay: Initial seconds to wait
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            current_delay = delay
            
            while attempt < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempt += 1
                    logger.warning(f"⚠️ Attempt {attempt} failed: {str(e)}")
                    
                    if attempt == retries:
                        logger.error("All retries exhausted.")
                        raise e # Re-raise the error to the API
                    
                    time.sleep(current_delay)
                    current_delay *= 2 # Exponential backoff (2s -> 4s -> 8s)
            return None
        return wrapper
    return decorator

# --- AI FUNCTIONS ---

@retry_with_backoff()
def generate_keywords(text: str):
    prompt = f"""
    Extract 5-10 SEO keywords from the text below.
    Return ONLY a raw JSON list of strings. No markdown, no "json" tags.
    Example output: ["python", "ai", "coding"]
    
    Text: {text}
    """
    response = model.generate_content(prompt)
    clean_text = response.text.strip().replace("```json", "").replace("```", "")
    result = json.loads(clean_text)
    # Logging response to the file
    log_interaction("Extract Keywords", text, result)
    return result

@retry_with_backoff()
def generate_bullet_points(text: str):
    prompt = f"""
    Convert the following text into concise bullet points.
    Return ONLY a raw JSON list of strings.
    Each string should start with an emoji (🔹).
    
    Text: {text}
    """
    response = model.generate_content(prompt)
    clean_text = response.text.strip().replace("```json", "").replace("```", "")
    result = json.loads(clean_text)
    log_interaction("Summarize Bullets", text, result)
    return result

@retry_with_backoff()
def analyze_sentiment(text: str):
    prompt = f"""
    Analyze the sentiment. Return JSON only: {{"sentiment": "POSITIVE/NEGATIVE", "score": 0.0-1.0}}
    
    Text: {text}
    """
    response = model.generate_content(prompt)
    clean_text = response.text.strip().replace("```json", "").replace("```", "")
    result = json.loads(clean_text)
    log_interaction("Sentiment Analysis", text, result)
    return result