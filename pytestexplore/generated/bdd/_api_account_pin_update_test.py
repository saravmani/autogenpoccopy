import pytest
import requests

BASE_URL = "http://localhost:8080"

@pytest.fixture
def valid_bearer_token():
    return "Bearer validBearerToken"

def test_successfully_update_account_pin(valid_bearer_token):
    headers = {"Authorization": valid_bearer_token}
    data = {
        "accountNumber": "thousand",
        "oldPin": "relate",
        "newPin": "remain",
        "password": "mWM8^WXpk!"
    }
    response = requests.post(f"{BASE_URL}/api/account/pin/update", json=data, headers=headers)
    assert response.status_code == 200
    assert response.json() == "PIN updated successfully"

def test_update_account_pin_with_incorrect_old_pin(valid_bearer_token):
    headers = {"Authorization": valid_bearer_token}
    data = {
        "accountNumber": "thousand",
        "oldPin": "incorrectPin",
        "newPin": "remain",
        "password": "mWM8^WXpk!"
    }
    response = requests.post(f"{BASE_URL}/api/account/pin/update", json=data, headers=headers)
    assert response.status_code == 400
    assert response.json() == "Incorrect old PIN"

def test_update_account_pin_with_unauthorized_access():
    data = {
        "accountNumber": "thousand",
        "oldPin": "relate",
        "newPin": "remain",
        "password": "mWM8^WXpk!"
    }
    response = requests.post(f"{BASE_URL}/api/account/pin/update", json=data)
    assert response.status_code == 401
    assert response.json() == "Unauthorized access"

def test_update_account_pin_with_invalid_new_pin_format(valid_bearer_token):
    headers = {"Authorization": valid_bearer_token}
    data = {
        "accountNumber": "thousand",
        "oldPin": "relate",
        "newPin": "short",
        "password": "mWM8^WXpk!"
    }
    response = requests.post(f"{BASE_URL}/api/account/pin/update", json=data, headers=headers)
    assert response.status_code == 400
    assert response.json() == "Invalid new PIN format"