import pytest
import requests

BASE_URL = "http://localhost:8080"

@pytest.fixture
def auth_token():
    # Assume successful login response
    response = requests.post(f"{BASE_URL}/api/users/login", json={
        "identifier": "user@example.com",
        "password": "Password123!"
    })
    assert response.status_code == 200
    return response.json()

def test_successful_fund_transfer(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    fund_transfer_data = {
        "sourceAccountNumber": "team",
        "targetAccountNumber": "everything",
        "amount": 966.27,
        "pin": "partner"
    }
    response = requests.post(f"{BASE_URL}/api/account/fund-transfer", json=fund_transfer_data, headers=headers)
    assert response.status_code == 200
    assert response.json().get("message") == "Fund transfer successful"

def test_fund_transfer_insufficient_balance(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    fund_transfer_data = {
        "sourceAccountNumber": "team",
        "targetAccountNumber": "everything",
        "amount": 966.27,
        "pin": "partner"
    }
    # Simulate insufficient balance
    response = requests.post(f"{BASE_URL}/api/account/fund-transfer", json=fund_transfer_data, headers=headers)
    assert response.status_code == 400
    assert response.json().get("error") == "Insufficient balance"

def test_fund_transfer_invalid_pin(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    fund_transfer_data = {
        "sourceAccountNumber": "team",
        "targetAccountNumber": "everything",
        "amount": 966.27,
        "pin": "wrongPin"
    }
    response = requests.post(f"{BASE_URL}/api/account/fund-transfer", json=fund_transfer_data, headers=headers)
    assert response.status_code == 401
    assert response.json().get("error") == "Invalid PIN"

def test_fund_transfer_non_existing_target(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    fund_transfer_data = {
        "sourceAccountNumber": "team",
        "targetAccountNumber": "nonExist",
        "amount": 966.27,
        "pin": "partner"
    }
    response = requests.post(f"{BASE_URL}/api/account/fund-transfer", json=fund_transfer_data, headers=headers)
    assert response.status_code == 404
    assert response.json().get("error") == "Target account not found"