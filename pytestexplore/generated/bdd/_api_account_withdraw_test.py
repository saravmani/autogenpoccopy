import pytest
import requests
import time

DELAY_SECONDS = 1
BASE_URL = "http://localhost:8080"
AUTH_CREDENTIALS = {
    "identifier": "genai_test_user@example.com",
    "password": "Secure#1234",
    "accountNumber": "856899",
    "pin": "1234"
}

def login():
    response = requests.post(f"{BASE_URL}/api/users/login", json={
        "identifier": AUTH_CREDENTIALS["identifier"],
        "password": AUTH_CREDENTIALS["password"]
    })
    return response.json()["token"]

@pytest.fixture
def auth_header():
    token = login()
    return {"Authorization": f"Bearer {token}"}

def test_successful_cash_withdrawal(auth_header):
    response = requests.post(f"{BASE_URL}/api/account/withdraw", headers=auth_header, json={
        "accountNumber": AUTH_CREDENTIALS["accountNumber"],
        "pin": AUTH_CREDENTIALS["pin"],
        "amount": 400
    })
    assert response.status_code == 200
    time.sleep(DELAY_SECONDS)

def test_withdrawal_insufficient_funds(auth_header):
    response = requests.post(f"{BASE_URL}/api/account/withdraw", headers=auth_header, json={
        "accountNumber": AUTH_CREDENTIALS["accountNumber"],
        "pin": AUTH_CREDENTIALS["pin"],
        "amount": 5000
    })
    assert response.status_code != 200
    time.sleep(DELAY_SECONDS)

def test_withdrawal_non_multiple_of_100(auth_header):
    response = requests.post(f"{BASE_URL}/api/account/withdraw", headers=auth_header, json={
        "accountNumber": AUTH_CREDENTIALS["accountNumber"],
        "pin": AUTH_CREDENTIALS["pin"],
        "amount": 411.06
    })
    assert response.status_code != 200
    time.sleep(DELAY_SECONDS)

def test_invalid_pin(auth_header):
    response = requests.post(f"{BASE_URL}/api/account/withdraw", headers=auth_header, json={
        "accountNumber": AUTH_CREDENTIALS["accountNumber"],
        "pin": "0000",
        "amount": 400
    })
    assert response.status_code != 200
    time.sleep(DELAY_SECONDS)

def test_unauthorized_withdrawal_attempt():
    response = requests.post(f"{BASE_URL}/api/account/withdraw", json={
        "accountNumber": AUTH_CREDENTIALS["accountNumber"],
        "pin": AUTH_CREDENTIALS["pin"],
        "amount": 400
    })
    assert response.status_code == 401
    time.sleep(DELAY_SECONDS)

def test_withdrawal_exceeding_maximum_limit(auth_header):
    response = requests.post(f"{BASE_URL}/api/account/withdraw", headers=auth_header, json={
        "accountNumber": AUTH_CREDENTIALS["accountNumber"],
        "pin": AUTH_CREDENTIALS["pin"],
        "amount": 150000
    })
    assert response.status_code != 200
    time.sleep(DELAY_SECONDS)