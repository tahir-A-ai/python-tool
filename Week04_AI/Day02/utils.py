import os
import json
import datetime
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Load Environment
# We use logic to find .env whether we are in root or Day02 folder
if os.path.exists(".env"):
    load_dotenv(".env")
elif os.path.exists("../.env"):
    load_dotenv("../.env")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("API Key not found! Check your .env file.")

genai.configure(api_key=api_key)

# Configuration
MODEL_NAME = "gemini-2.5-flash"
LOG_FILE = "prompt_logs.json"

def log_interaction(task_type, prompt, response):
    """Saves the interaction to a JSON log file."""
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "task_type": task_type,
        "model": MODEL_NAME,
        "prompt": prompt,
        "response": response
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

def ask_gemini(task_type, prompt):
    """
    Sends the prompt to Gemini and logs the result.
    Returns the clean text response.
    """
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        text_response = response.text.strip()
        
        # Auto-log every success
        log_interaction(task_type, prompt, text_response)
        
        return text_response
    except Exception as e:
        return f"Error: {str(e)}"