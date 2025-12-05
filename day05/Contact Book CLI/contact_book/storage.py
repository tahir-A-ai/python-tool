import json
import os

DATA_FILE = os.path.join("data", "contacts.json")


def load_contacts():
    """Load contacts list from JSON file."""
    if not os.path.exists("data"):
        os.makedirs("data")

    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump([], f)

    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []


def save_contacts(contacts):
    """Save list of contacts into JSON file."""
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(contacts, f, indent=4)
    except Exception:
        print("Error saving contacts.")
