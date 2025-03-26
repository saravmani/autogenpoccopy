import pytest
import requests
import time

DELAY_SECONDS = 1
BASE_URL = "http://localhost:8080"
AUTH_URL = f"{BASE_URL}/api/users/login"

def get_bearer_token():
    response = requests.post(AUTH_URL, json={
        "identifier": "genai_test_user@example.com",
        "password": "Secure#1234"
    })
    return response.json().get("token")

@pytest.fixture(scope="module")
def bearer_token():
    return get_bearer_token()

def test_successful_fund_transfer(bearer_token):
    headers = {"Authorization": f"Bearer {bearer_token}"}
    data = {
        "sourceAccountNumber": "fall",
        "targetAccountNumber": "enough",
        "amount": 500,
        "pin": "1234"
    }
    response = requests.post(f"{BASE_URL}/api/account/fund-transfer", json=data, headers=headers)
    assert response.status_code == 200
    time.sleep(DELAY_SECONDS)

def test_insufficient_funds_for_transfer(bearer_token):
    headers = {"Authorization": f"Bearer {bearer_token}"}
    data = {
        "sourceAccountNumber": "fall",
        "targetAccountNumber": "enough",
        "amount": 1000000,  # Exceeding the assumed account balance for test
        "pin": "1234"
    }
    response = requests.post(f"{BASE_URL}/api/account/fund-transfer", json=data, headers=headers)
    assert response.status_code == 400
    time.sleep(DELAY_SECONDS)

def test_invalid_pin_for_fund_transfer(bearer_token):
    headers = {"Authorization": f"Bearer {bearer_token}"}
    data = {
        "sourceAccountNumber": "fall",
        "targetAccountNumber": "enough",
        "amount": 500,
        "pin": "0000"  # Invalid PIN
    }
    response = requests.post(f"{BASE_URL}/api/account/fund-transfer", json=data, headers=headers)
    assert response.status_code == 400
    time.sleep(DELAY_SECONDS)

def test_invalid_authentication_token():
    headers = {"Authorization": "Bearer invalid-token"}
    data = {
        "sourceAccountNumber": "fall",
        "targetAccountNumber": "enough",
        "amount": 500,
        "pin": "1234"
    }
    response = requests.post(f"{BASE_URL}/api/account/fund-transfer", json=data, headers=headers)
    assert response.status_code == 401
    time.sleep(DELAY_SECONDS)

def test_transfer_amount_not_multiple_of_100(bearer_token):
    headers = {"Authorization": f"Bearer {bearer_token}"}
    data = {
        "sourceAccountNumber": "fall",
        "targetAccountNumber": "enough",
        "amount": 568.62,  # Amount not in multiples of 100
        "pin": "1234"
    }
    response = requests.post(f"{BASE_URL}/api/account/fund-transfer", json=data, headers=headers)
    assert response.status_code == 400
    time.sleep(DELAY_SECONDS)

def test_transfer_to_same_account(bearer_token):
    headers = {"Authorization": f"Bearer {bearer_token}"}
    data = {
        "sourceAccountNumber": "fall",
        "targetAccountNumber": "fall",  # Same account number for source and target
        "amount": 500,
        "pin": "1234"
    }
    response = requests.post(f"{BASE_URL}/api/account/fund-transfer", json=data, headers=headers)
    assert response.status_code == 400
    time.sleep(DELAY_SECONDS)