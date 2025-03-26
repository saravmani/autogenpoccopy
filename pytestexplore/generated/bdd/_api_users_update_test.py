import pytest
import requests
import time

DELAY_SECONDS = 1
BASE_URL = "http://localhost:8080"
TOKEN_URL = f"{BASE_URL}/api/users/login"
USER_UPDATE_URL = f"{BASE_URL}/api/users/update"

def get_bearer_token():
    response = requests.post(TOKEN_URL, json={
        "identifier": "genai_test_user@example.com",
        "password": "Secure#1234"
    })
    return response.json().get("token")

def test_successful_update_user_details():
    token = get_bearer_token()
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "id": 759,
        "name": "updatedName",
        "email": "updatedEmail",
        "countryCode": "newCountry",
        "phoneNumber": "newPhone",
        "address": "newEnvironment"
    }
    response = requests.post(USER_UPDATE_URL, headers=headers, json=payload)
    assert response.status_code == 200
    time.sleep(DELAY_SECONDS)

def test_update_user_details_invalid_token():
    headers = {"Authorization": "Bearer invalidtoken"}
    payload = {
        "id": 759,
        "name": "updatedName",
        "email": "updatedEmail",
        "countryCode": "newCountry",
        "phoneNumber": "newPhone"
    }
    response = requests.post(USER_UPDATE_URL, headers=headers, json=payload)
    assert response.status_code == 401
    time.sleep(DELAY_SECONDS)

def test_update_user_details_missing_fields():
    token = get_bearer_token()
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "id": 759,
        "name": "updatedName",
        "countryCode": "newCountry",
        "phoneNumber": "newPhone",
        "address": "newEnvironment"
    }
    response = requests.post(USER_UPDATE_URL, headers=headers, json=payload)
    assert response.status_code == 400
    time.sleep(DELAY_SECONDS)