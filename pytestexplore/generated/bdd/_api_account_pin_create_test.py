import pytest
import requests

BASE_URL = "http://localhost:8080"
AUTH_TOKEN = "Bearer valid_auth_token"  # Replace with a valid token for setup

@pytest.fixture
def headers():
    return {"Authorization": AUTH_TOKEN, "Content-Type": "application/json"}

def test_success_create_pin(headers):
    data = {
        "accountNumber": "1234567890",
        "pin": "1234",
        "password": "_#61ZRiE#1"
    }
    response = requests.post(f"{BASE_URL}/api/account/pin/create", json=data, headers=headers)
    assert response.status_code == 200
    assert response.json() == "Success"

def test_fail_create_duplicate_pin(headers):
    # Pre-setup: Create PIN first time
    data = {
        "accountNumber": "1234567890",
        "pin": "1234",
        "password": "_#61ZRiE#1"
    }
    requests.post(f"{BASE_URL}/api/account/pin/create", json=data, headers=headers)

    # Attempt to create duplicate PIN
    response = requests.post(f"{BASE_URL}/api/account/pin/create", json=data, headers=headers)
    assert response.status_code == 400
    assert response.json() == "Error: Duplicate PIN creation"

def test_fail_create_pin_invalid_password(headers):
    data = {
        "accountNumber": "1234567890",
        "pin": "1234",
        "password": "password123"
    }
    response = requests.post(f"{BASE_URL}/api/account/pin/create", json=data, headers=headers)
    assert response.status_code == 401
    assert response.json() == "Error: Invalid password"

def test_fail_create_pin_missing_field(headers):
    data = {
        "accountNumber": "1234567890",
        "password": "_#61ZRiE#1"
    }
    response = requests.post(f"{BASE_URL}/api/account/pin/create", json=data, headers=headers)
    assert response.status_code == 400
    assert response.json() == "Error: Missing pin field"