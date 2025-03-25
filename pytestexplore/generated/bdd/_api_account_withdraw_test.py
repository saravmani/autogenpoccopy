import pytest
import requests

BASE_URL = "http://localhost:8080"

def test_successful_withdrawal():
    # Setup: Ensure account has sufficient balance
    token = "valid_token"  # Assume valid bearer token is available
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "accountNumber": "123456",
        "pin": "owner",
        "amount": 267.67
    }
    response = requests.post(f"{BASE_URL}/api/account/withdraw", json=data, headers=headers)
    
    assert response.status_code == 200
    assert response.json().get("status") == "success"

def test_withdrawal_insufficient_balance():
    # Setup: Ensure account has insufficient balance
    token = "valid_token"
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "accountNumber": "123456",
        "pin": "owner",
        "amount": 267.67
    }
    response = requests.post(f"{BASE_URL}/api/account/withdraw", json=data, headers=headers)
    
    assert response.status_code == 400
    assert "insufficient funds" in response.text

def test_withdrawal_invalid_account_number():
    token = "valid_token"
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "accountNumber": "invalid",
        "pin": "owner",
        "amount": 267.67
    }
    response = requests.post(f"{BASE_URL}/api/account/withdraw", json=data, headers=headers)
    
    assert response.status_code == 400
    assert "invalid account number" in response.text

def test_withdrawal_incorrect_pin():
    token = "valid_token"
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "accountNumber": "123456",
        "pin": "wrong",
        "amount": 100
    }
    response = requests.post(f"{BASE_URL}/api/account/withdraw", json=data, headers=headers)
    
    assert response.status_code == 400
    assert "incorrect PIN" in response.text

def test_duplicate_withdrawal_request():
    token = "valid_token"
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "accountNumber": "123456",
        "pin": "owner",
        "amount": 267.67
    }
    # Assume first request is successful
    requests.post(f"{BASE_URL}/api/account/withdraw", json=data, headers=headers)
    
    # Test duplicate request
    response = requests.post(f"{BASE_URL}/api/account/withdraw", json=data, headers=headers)
    
    assert response.status_code == 400
    assert "duplicate request" in response.text

def test_unauthorized_access_missing_token():
    data = {
        "accountNumber": "123456",
        "pin": "owner",
        "amount": 100
    }
    response = requests.post(f"{BASE_URL}/api/account/withdraw", json=data)
    
    assert response.status_code == 401
    assert "unauthorized access" in response.text