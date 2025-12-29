import httpx
import random
import string

# config
BASE_URL = "http://127.0.0.1:8000"

# Registration
def run_consumer():
    random_str = ''.join(random.choices(string.ascii_lowercase, k=5))
    email = f"user_{random_str}@consumer.com"
    password = "securepassword123"
    data = {"email":email, "password":password}
    response = httpx.post(f"{BASE_URL}/users", json=data)
    if response.status_code != 200:
        print("Registration failed.", {response.text})
        return
    else:
        print("User registered successfully!")

    # Login
    login_response = httpx.post(f"{BASE_URL}/token", data={"username": email, "password": password})
    if login_response.status_code != 200:
        print("Login Failed.", {login_response.text})
        return
    
    print("Logged in successfully!")
    # Extract the token string
    token_data = login_response.json()
    access_token = token_data["access_token"]
    print(f"Got Token: {access_token[:20]}...")
    # access protected endpoints
    print("Accessing Protected Endpoint (/users/me)...")
    # attaching the header
    auth_headers = {
            "Authorization": f"Bearer {access_token}"
        }

    # sending the headers with the request
    me_response = httpx.get(f"{BASE_URL}/users/me", headers=auth_headers)
    print(f"Response Status: {me_response.status_code}")
    print(f"Response Data: {me_response.json()}")

    # creating a task
    print("Creating a Task via API...") 
    task_data = {
            "title": "Learning about Consumer Script in fastapi",
            "description": f"Created by {email}",
            "is_completed": False
        }
    task_response = httpx.post(f"{BASE_URL}/tasks", json=task_data, headers=auth_headers)
    print(f"Task Created: {task_response.json()}")

# Main()
if __name__ == "__main__":
    run_consumer()

