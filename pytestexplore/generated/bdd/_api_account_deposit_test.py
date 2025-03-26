Here are pytest test cases for the given scenarios:


import pytest
import requests
import time

DELAY_SECONDS = 1
BASE_URL = "http://localhost:8080"

@pytest.fixture
def get_bearer_token():
    response = requests.post(f"{BASE_URL}/api/users/login", json={
        "identifier": "genai_test_user@example.com",
        "password": "Secure#1234"
    })
    token = response.json().get('token')
    assert response.status_code == 200
    return token

def test_successful_cash_deposit(get_bearer_token):
    headers = {"Authorization": f"Bearer {get_bearer_token}"}
    response = requests.post(f"{BASE_URL}/api/account/deposit", headers=headers, json={
        "accountNumber": "856899",
        "pin": "1234",
        "amount": 500
    })
    assert response.status_code == 200
    time.sleep(DELAY_SECONDS)

def test_deposit_amount_greater_than_100000(get_bearer_token):
    headers = {"Authorization": f"Bearer {get_bearer_token}"}
    response = requests.post(f"{BASE_URL}/api/account/deposit", headers=headers, json={
        "accountNumber": "856899",
        "pin": "1234",
        "amount": 100500
    })
    assert response.status_code != 200
    time.sleep(DELAY_SECONDS)

def test_deposit_invalid_amount_not_in_multiples_of_100(get_bearer_token):
    headers = {"Authorization": f"Bearer {get_bearer_token}"}
    response = requests.post(f"{BASE_URL}/api/account/deposit", headers=headers, json={
        "accountNumber": "856899",
        "pin": "1234",
        "amount": 527
    })
    assert response.status_code != 200
    time.sleep(DELAY_SECONDS)

def test_deposit_amount_less_than_or_equal_zero(get_bearer_token):
    headers = {"Authorization": f"Bearer {get_bearer_token}"}
    response = requests.post(f"{BASE_URL}/api/account/deposit", headers=headers, json={
        "accountNumber": "856899",
        "pin": "1234",
        "amount": 0
    })
    assert response.status_code != 200
    time.sleep(DELAY_SECONDS)

def test_deposit_invalid_authentication_token():
    headers = {"Authorization": "Bearer invalid_token"}
    response = requests.post(f"{BASE_URL}/api/account/deposit", headers=headers, json={
        "accountNumber": "856899",
        "pin": "1234",
        "amount": 500
    })
    assert response.status_code == 401
    time.sleep(DELAY_SECONDS)