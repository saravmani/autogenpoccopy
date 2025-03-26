 

import pytest
from pytest_bdd import given
import requests
import time

DELAY_SECONDS = 1
BASE_URL = "http://localhost:8080"
ACCOUNT_NUMBER = "856899"
PIN = "1234"
PASSWORD = "Secure#1234"
IDENTIFIER = "genai_test_user@example.com"


@given("has a valid bearer token")
def get_bearer_token(identifier, password):
    response = requests.post(f"{BASE_URL}/api/users/login", json={"identifier": identifier, "password": password})
    return response.json().get("token")

@pytest.fixture(scope='module')
def bearer_token():
    return get_bearer_token(IDENTIFIER, PASSWORD)

def test_successful_create_pin(bearer_token):
    payload = {"accountNumber": ACCOUNT_NUMBER, "pin": PIN, "password": PASSWORD}
    headers = {"Authorization": f"Bearer {bearer_token}"}
    response = requests.post(f"{BASE_URL}/api/account/pin/create", json=payload, headers=headers)
    assert response.status_code == 200
    time.sleep(DELAY_SECONDS)

def test_fail_create_pin_invalid_token():
    payload = {"accountNumber": ACCOUNT_NUMBER, "pin": PIN, "password": PASSWORD}
    headers = {"Authorization": "Bearer invalid_token"}
    response = requests.post(f"{BASE_URL}/api/account/pin/create", json=payload, headers=headers)
    assert response.status_code == 401
    time.sleep(DELAY_SECONDS)

def test_fail_create_pin_duplicate(bearer_token):
    # Pre-setup: Create PIN successfully first
    payload = {"accountNumber": ACCOUNT_NUMBER, "pin": PIN, "password": PASSWORD}
    headers = {"Authorization": f"Bearer {bearer_token}"}
    requests.post(f"{BASE_URL}/api/account/pin/create", json=payload, headers=headers)

    # Try creating the same PIN again
    response = requests.post(f"{BASE_URL}/api/account/pin/create", json=payload, headers=headers)
    assert response.status_code != 200
    time.sleep(DELAY_SECONDS)

def test_fail_create_pin_missing_fields(bearer_token):
    payload = {"accountNumber": ACCOUNT_NUMBER, "password": PASSWORD}  # Missing "pin"
    headers = {"Authorization": f"Bearer {bearer_token}"}
    response = requests.post(f"{BASE_URL}/api/account/pin/create", json=payload, headers=headers)
    assert response.status_code == 400
    time.sleep(DELAY_SECONDS)


### Notes:
- `get_bearer_token` is a helper function to obtain a token for simplicity.
- Each test case corresponds to one of the BDD scenarios.
- `bearer_token` is a fixture used to get a valid Bearer token, scoped at the module level for reuse across tests without re-authenticating each time.
- The tests use the `pytest` framework with the `requests` library and include a delay after each test for demonstration purposes.