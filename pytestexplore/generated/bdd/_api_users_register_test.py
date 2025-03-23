import pytest
import requests

BASE_URL = "http://localhost:8080/api/users"

@pytest.fixture
def prepare_existing_user():
    existing_user_data = {
        "name": "John Existing",
        "password": "strongP@ssw0rd",
        "email": "john.existing@gmail.com",
        "countryCode": "IN",
        "phoneNumber": "9999999999",
        "address": "123 Existing St"
    }
    requests.post(f"{BASE_URL}/register", json=existing_user_data)

def test_successfully_register_new_user():
    new_user_data = {
        "name": "John Doe",
        "password": "P@ssw0rd123!",
        "email": "john.doe@gmail.com",
        "countryCode": "IN",
        "phoneNumber": "9876543210",
        "address": "123 Elm Street"
    }
    response = requests.post(f"{BASE_URL}/register", json=new_user_data)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["name"] == "John Doe"
    assert response_data["email"] == "john.doe@gmail.com"
    assert response_data["countryCode"] == "IN"
    assert response_data["phoneNumber"] == "9876543210"
    assert response_data["address"] == "123 Elm Street"

def test_registration_fails_due_to_existing_email(prepare_existing_user):
    conflicting_user_data = {
        "name": "Jane Smith",
        "password": "Example$123!",
        "email": "john.existing@gmail.com",
        "countryCode": "IN",
        "phoneNumber": "1234567890",
        "address": "456 Oak Avenue"
    }
    response = requests.post(f"{BASE_URL}/register", json=conflicting_user_data)
    assert response.status_code == 400
    assert response.text == "Email already exists"

def test_registration_fails_due_to_existing_phone_number(prepare_existing_user):
    conflicting_user_data = {
        "name": "Mike Ross",
        "password": "Secure$345!",
        "email": "mike.ross@gmail.com",
        "countryCode": "IN",
        "phoneNumber": "9999999999",
        "address": "789 Pine Road"
    }
    response = requests.post(f"{BASE_URL}/register", json=conflicting_user_data)
    assert response.status_code == 400
    assert response.text == "Phone number already exists"

def test_registration_fails_due_to_invalid_password_policy():
    weak_password_user_data = {
        "name": "Weak Password",
        "password": "weakpass",
        "email": "weak.pass@gmail.com",
        "countryCode": "IN",
        "phoneNumber": "0987654321",
        "address": "321 Birch Lane"
    }
    response = requests.post(f"{BASE_URL}/register", json=weak_password_user_data)
    assert response.status_code == 400

def test_registration_fails_due_to_missing_required_fields():
    missing_fields_user_data = {
        "name": "Missing Details",
        "password": "MissingPass1!",
        "email": "",
        "countryCode": "IN",
        "phoneNumber": "",
        "address": ""
    }
    response = requests.post(f"{BASE_URL}/register", json=missing_fields_user_data)
    assert response.status_code == 400

 