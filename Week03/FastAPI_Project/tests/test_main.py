from http import client
from fastapi.testclient import TestClient
from main import app
import random
import string

client = TestClient(app)

# helper function to generate random emails everytime test-cases runs
def random_email():
    # Generates a random string like "x7k9p@test.com"
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
    return f"{random_str}@test.com"

# test-case for creating new user
def test_create_user():
    email = random_email()
    data = {"email": email, "password":"test12345"}
    response = client.post('/users', json=data)

    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["email"] == email


# test-case for user login
def test_login_success():
    test_email = random_email()
    test_password = "password123"
    
    # Create the user (ignoring the response here, we assume it works from previous test)
    client.post("/users", json={"email": test_email, "password": test_password})

    # IMPORTANT: We use 'data=' for Form Data, not 'json='
    # The key nust be 'username', as email is our username
    login_data = {
        "username": test_email, 
        "password": test_password
    }

    response = client.post("/token", data=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"
