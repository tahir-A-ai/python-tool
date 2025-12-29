import requests
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Repository

# Configuration for the AI Service
# Note: In production, this URL should come from settings.py or .env
AI_ENGINE_URL = "http://127.0.0.1:8001/ingest"

@receiver(post_save, sender=Repository)
def trigger_ai_ingestion(sender, instance, created, **kwargs):
    """
    Triggered automatically after a Repository is saved.
    If it's a new upload (created=True), it sends the file path to FastAPI.
    """
    if created:
        print(f"New Repository detected: {instance.name}. Triggering AI Engine...")
        
        # Prepare the data packet for FastAPI
        payload = {
            "repo_id": instance.id,
            "file_path": instance.repo_files.path  # Sends the absolute path on disk
        }
        print(payload)

        try:
            # Send POST request to FastAPI
            response = requests.post(AI_ENGINE_URL, json=payload, timeout=5)
            
            if response.status_code == 200:
                print(f"Ingestion started successfully for Repo ID: {instance.id}")
            else:
                print(f"FastAPI refused request: {response.status_code} - {response.text}")

        except requests.exceptions.ConnectionError:
            print(f"Connection Failed: Could not connect to AI Engine at {AI_ENGINE_URL}. Is it running?")
        except Exception as e:
            print(f"Unexpected Error during connection with FastAPI (AI_ENGINE_URL): {str(e)}")