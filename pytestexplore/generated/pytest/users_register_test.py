import pytest
import requests

BASE_URL = "http://localhost:8080"

@pytest.fixture
def user_data():
    return {
        "name": "Test User",
        "password": "Password@123",
        "email": "testuser@example.com",
        "countryCode": "IN",
        "phoneNumber": "9999999999",
        "address": "123 Test Street"
    }

def test_register_user_success(user_data):
    response = requests.post(f"{BASE_URL}/api/users/register", json=user_data)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["name"] == user_data["name"]
    assert response_data["email"] == user_data["email"]
    assert response_data["countryCode"] == "IN"
    assert response_data["phoneNumber"] == user_data["phoneNumber"]
    assert "accountNumber" in response_data

def test_register_user_duplicate_email(user_data):
    # Presetup: Register the user once
    requests.post(f"{BASE_URL}/api/users/register", json=user_data)
    # Attempt registering a second time with the same email
    response = requests.post(f"{BASE_URL}/api/users/register", json=user_data)
    assert response.status_code == 400
    assert response.text == "Email already exists"

def test_register_user_duplicate_phone(user_data):
    # Presetup: Register the user once
    requests.post(f"{BASE_URL}/api/users/register", json=user_data)
    # Modify email to ensure uniqueness, keep phone the same
    user_data["email"] = "uniqueemail@example.com"
    response = requests.post(f"{BASE_URL}/api/users/register", json=user_data)
    assert response.status_code == 400
    assert response.text == "Phone number already exists"

def test_register_user_invalid_password(user_data):
    user_data["password"] = "simple"
    response = requests.post(f"{BASE_URL}/api/users/register", json=user_data)
    assert response.status_code == 400

 