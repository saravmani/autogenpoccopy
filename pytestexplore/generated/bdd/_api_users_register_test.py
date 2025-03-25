Here's the pytest code for the given BDD scenarios:


import pytest
import requests

BASE_URL = "http://localhost:8080"

@pytest.fixture
def create_user():
    def _create_user(user_data):
        response = requests.post(f"{BASE_URL}/api/users/register", json=user_data)
        return response
    return _create_user

def test_successful_registration(create_user):
    user_details = {
        "name": "John Doe",
        "password": "Secure#1234",
        "email": "john.doe@example.com",
        "countryCode": "IN",
        "phoneNumber": "9876543210",
        "address": "123 Main St, New Delhi"
    }
    response = create_user(user_details)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["name"] == "John Doe"
    assert response_data["email"] == "john.doe@example.com"
    assert response_data["countryCode"] == "IN"
    assert response_data["phoneNumber"] == "9876543210"
    assert response_data["address"] == "123 Main St, New Delhi"

def test_registration_duplicate_phone_number(create_user):
    existing_user = {
        "name": "Existing User",
        "password": "Secure#1234",
        "email": "existing.user@example.com",
        "countryCode": "IN",
        "phoneNumber": "9876543210",
        "address": "123 Main St, New Delhi"
    }
    create_user(existing_user)  # Preset an existing user
    
    duplicate_user = {
        "name": "Jane Doe",
        "password": "AnotherSecure#1234",
        "email": "jane.doe@example.com",
        "countryCode": "IN",
        "phoneNumber": "9876543210",
        "address": "456 Second St, Mumbai"
    }
    response = create_user(duplicate_user)
    assert response.status_code == 400
    assert response.text == "Phone number already exists"

def test_registration_duplicate_email(create_user):
    existing_user = {
        "name": "Existing User",
        "password": "Secure#1234",
        "email": "jane.doe@example.com",
        "countryCode": "IN",
        "phoneNumber": "9876549999",
        "address": "123 Main St, New Delhi"
    }
    create_user(existing_user)  # Preset an existing user
    
    duplicate_email_user = {
        "name": "Jim Doe",
        "password": "GoodPass#5678",
        "email": "jane.doe@example.com",
        "countryCode": "IN",
        "phoneNumber": "9876543219",
        "address": "789 Third St, Chennai"
    }
    response = create_user(duplicate_email_user)
    assert response.status_code == 400
    assert response.text == "Email already exists"

def test_registration_invalid_password(create_user):
    invalid_password_user = {
        "name": "Jake Doe",
        "password": "simplepass",
        "email": "jake.doe@example.com",
        "countryCode": "IN",
        "phoneNumber": "9876543220",
        "address": "101 First St, Kolkata"
    }
    response = create_user(invalid_password_user)
    assert response.status_code == 400

def test_registration_invalid_phone_number_length(create_user):
    invalid_phone_user = {
        "name": "Lara Doe",
        "password": "Complex#1234",
        "email": "lara.doe@example.com",
        "countryCode": "IN",
        "phoneNumber": "98765",
        "address": "303 Fourth St, Bangalore"
    }
    response = create_user(invalid_phone_user)
    assert response.status_code == 400