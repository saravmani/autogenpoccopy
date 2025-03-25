import pytest
import requests

BASE_URL = "http://localhost:8080"

def test_successful_cash_deposit():
    token = "valid-auth-token"  # Replace with a valid auth token
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "accountNumber": "1234567890",
        "pin": "1234",
        "amount": 195.94
    }
    response = requests.post(f"{BASE_URL}/api/account/deposit", json=data, headers=headers)
    assert response.status_code == 200
    assert response.text == "Deposit successful"

def test_deposit_with_invalid_account_number():
    token = "valid-auth-token"  # Replace with a valid auth token
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "accountNumber": "9999999999",
        "pin": "1234",
        "amount": 200.00
    }
    response = requests.post(f"{BASE_URL}/api/account/deposit", json=data, headers=headers)
    assert response.status_code == 400
    assert response.text == "Invalid account number"

def test_deposit_with_incorrect_pin():
    token = "valid-auth-token"  # Replace with a valid auth token
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "accountNumber": "1234567890",
        "pin": "0000",
        "amount": 100.00
    }
    response = requests.post(f"{BASE_URL}/api/account/deposit", json=data, headers=headers)
    assert response.status_code == 400
    assert response.text == "Incorrect pin"

def test_deposit_without_authentication_token():
    data = {
        "accountNumber": "1234567890",
        "pin": "1234",
        "amount": 150.00
    }
    response = requests.post(f"{BASE_URL}/api/account/deposit", json=data)
    assert response.status_code == 401
    assert response.text == "Authentication required"

def test_deposit_with_invalid_amount_format():
    token = "valid-auth-token"  # Replace with a valid auth token
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "accountNumber": "1234567890",
        "pin": "1234",
        "amount": "ABC"
    }
    response = requests.post(f"{BASE_URL}/api/account/deposit", json=data, headers=headers)
    assert response.status_code == 400
    assert response.text == "Invalid amount format"