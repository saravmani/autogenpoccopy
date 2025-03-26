import pytest
import requests
import time

DELAY_SECONDS = 1
BASE_URL = "http://localhost:8080"

def test_successful_user_registration():
    payload = {
        "name": "John Doe",
        "password": "Pass#1234567",
        "email": "john.doe@example.com",
        "countryCode": "IN",
        "phoneNumber": "1234567890",
        "address": "123 Elm Street, NYC"
    }
    response = requests.post(f"{BASE_URL}/api/users/register", json=payload)
    assert response.status_code == 200
    time.sleep(DELAY_SECONDS)

def test_duplicate_email_registration():
    # Pre-setup: Register the user first
    payload = {
        "name": "John Doe",
        "password": "Pass#1234567",
        "email": "john.doe@example.com",
        "countryCode": "IN",
        "phoneNumber": "1234567890",
        "address": "123 Elm Street, NYC"
    }
    requests.post(f"{BASE_URL}/api/users/register", json=payload)

    # Attempt duplicate registration
    payload = {
        "name": "Jane Doe",
        "password": "Pass#1234567",
        "email": "john.doe@example.com",
        "countryCode": "IN",
        "phoneNumber": "1234567891",
        "address": "456 Oak Street, LA"
    }
    response = requests.post(f"{BASE_URL}/api/users/register", json=payload)
    assert response.status_code == 400
    time.sleep(DELAY_SECONDS)

def test_duplicate_phone_number_registration():
    # Pre-setup: Register the user first
    payload = {
        "name": "John Doe",
        "password": "Pass#1234567",
        "email": "john.doe@example.com",
        "countryCode": "IN",
        "phoneNumber": "1234567890",
        "address": "123 Elm Street, NYC"
    }
    requests.post(f"{BASE_URL}/api/users/register", json=payload)

    # Attempt duplicate registration with same phone number
    payload = {
        "name": "Jane Smith",
        "password": "Pass#1234567",
        "email": "jane.smith@example.com",
        "countryCode": "IN",
        "phoneNumber": "1234567890",
        "address": "789 Pine Street, SF"
    }
    response = requests.post(f"{BASE_URL}/api/users/register", json=payload)
    assert response.status_code == 400
    time.sleep(DELAY_SECONDS)

def test_invalid_password_registration():
    payload = {
        "name": "Bob Brown",
        "password": "pass123",
        "email": "bob.brown@example.com",
        "countryCode": "IN",
        "phoneNumber": "9876543210",
        "address": "321 Maple Street, DC"
    }
    response = requests.post(f"{BASE_URL}/api/users/register", json=payload)
    assert response.status_code == 400
    time.sleep(DELAY_SECONDS)

def test_missing_required_fields_registration():
    payload = {
        "name": "missingName",
        "password": "Pass#1234567",
        "email": "myemail@example.com",
        "countryCode": "IN",
        "phoneNumber": "1230984567",
        "address": ""
    }
    response = requests.post(f"{BASE_URL}/api/users/register", json=payload)
    assert response.status_code == 400
    time.sleep(DELAY_SECONDS)

if __name__ == "__main__":
    pytest.main()