import pytest
import requests
import time

DELAY_SECONDS = 1
BASE_URL = "http://localhost:8080"

def get_valid_token():
    login_response = requests.post(f"{BASE_URL}/api/users/login", json={
        "identifier": "genai_test_user@example.com",
        "password": "Secure#1234"
    })
    return login_response.json().get("token")

def test_successful_deposit():
    token = get_valid_token()
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "accountNumber": "856899",
        "pin": "1234",
        "amount": 1000
    }
    response = requests.post(f"{BASE_URL}/api/account/deposit", json=data, headers=headers)
    assert response.status_code == 200
    time.sleep(DELAY_SECONDS)

def test_deposit_invalid_token():
    headers = {"Authorization": "Bearer invalid_token"}
    data = {
        "accountNumber": "856899",
        "pin": "1234",
        "amount": 1000
    }
    response = requests.post(f"{BASE_URL}/api/account/deposit", json=data, headers=headers)
    assert response.status_code == 401
    time.sleep(DELAY_SECONDS)

def test_deposit_amount_greater_than_100000():
    token = get_valid_token()
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "accountNumber": "856899",
        "pin": "1234",
        "amount": 1000001
    }
    response = requests.post(f"{BASE_URL}/api/account/deposit", json=data, headers=headers)
    assert response.status_code == 400
    time.sleep(DELAY_SECONDS)

def test_deposit_amount_not_multiple_of_100():
    token = get_valid_token()
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "accountNumber": "856899",
        "pin": "1234",
        "amount": 1050
    }
    response = requests.post(f"{BASE_URL}/api/account/deposit", json=data, headers=headers)
    assert response.status_code == 400
    time.sleep(DELAY_SECONDS)

def test_deposit_amount_zero():
    token = get_valid_token()
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "accountNumber": "856899",
        "pin": "1234",
        "amount": 0
    }
    response = requests.post(f"{BASE_URL}/api/account/deposit", json=data, headers=headers)
    assert response.status_code == 400
    time.sleep(DELAY_SECONDS)