import pytest
import requests

BASE_URL = "http://localhost:8080"

@pytest.fixture
def valid_token():
    # Simulated method to get a valid token
    response = requests.post(f"{BASE_URL}/api/users/login", json={
        "identifier": "valid_user",
        "password": "valid_password"
    })
    return response.text if response.status_code == 200 else None

@pytest.fixture
def create_user_679():
    # Assume code exists to create and ensure user 679 exists
    return 679

@pytest.fixture
def create_user_680():
    # Assume code exists to create and ensure user 680 with "administration" email exists
    return 680

def test_successful_user_update(create_user_679, valid_token):
    headers = {"Authorization": f"Bearer {valid_token}"}
    data = {
        "id": 679,
        "name": "increase",
        "password": "Fu%0Pny5HR",
        "email": "administration",
        "countryCode": "explain",
        "phoneNumber": "myself",
        "address": "easy"
    }
    response = requests.patch(f"{BASE_URL}/api/users/update", headers=headers, json=data)
    assert response.status_code == 200
    assert "success" in response.text.lower()

def test_unauthorized_access_without_token(create_user_679):
    data = {
        "id": 679,
        "name": "increase",
    }
    response = requests.patch(f"{BASE_URL}/api/users/update", json=data)
    assert response.status_code == 401
    assert "authentication failure" in response.text.lower()

def test_update_with_invalid_email(create_user_679, valid_token):
    headers = {"Authorization": f"Bearer {valid_token}"}
    data = {
        "id": 679,
        "name": "increase",
        "password": "Fu%0Pny5HR",
        "email": "invalid-email",
    }
    response = requests.patch(f"{BASE_URL}/api/users/update", headers=headers, json=data)
    assert response.status_code == 400
    assert "email validation failure" in response.text.lower()

def test_update_with_existing_email(create_user_679, create_user_680, valid_token):
    headers = {"Authorization": f"Bearer {valid_token}"}
    data = {
        "id": 679,
        "name": "increase",
        "password": "Fu%0Pny5HR",
        "email": "administration",
    }
    response = requests.patch(f"{BASE_URL}/api/users/update", headers=headers, json=data)
    assert response.status_code == 400
    assert "email already exists" in response.text.lower()

def test_update_with_missing_fields(create_user_679, valid_token):
    headers = {"Authorization": f"Bearer {valid_token}"}
    data = {"id": 679}  # Missing other required fields
    response = requests.patch(f"{BASE_URL}/api/users/update", headers=headers, json=data)
    assert response.status_code == 400
    assert "field validation errors" in response.text.lower()