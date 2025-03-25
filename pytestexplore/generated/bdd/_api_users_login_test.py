import pytest
import requests

BASE_URL = "http://localhost:8080"

def test_successful_login():
    data = {"identifier": "daughter", "password": "Hx%4L7sy*M"}
    response = requests.post(f"{BASE_URL}/api/users/login", json=data)
    assert response.status_code == 200
    token = response.json().get("token")
    assert token is not None

def test_unsuccessful_login_invalid_credentials():
    data = {"identifier": "daughter", "password": "wrongPassword123!"}
    response = requests.post(f"{BASE_URL}/api/users/login", json=data)
    assert response.status_code == 401
    assert response.text == "Invalid credentials"

def test_unsuccessful_login_missing_password():
    data = {"identifier": "daughter"}
    response = requests.post(f"{BASE_URL}/api/users/login", json=data)
    assert response.status_code == 400
    assert response.text == "Password is required"

def test_unsuccessful_login_missing_identifier():
    data = {"password": "Hx%4L7sy*M"}
    response = requests.post(f"{BASE_URL}/api/users/login", json=data)
    assert response.status_code == 400
    assert response.text == "Identifier is required"

def test_unsuccessful_login_invalid_identifier_type():
    data = {"identifier": 123456, "password": "Hx%4L7sy*M"}
    response = requests.post(f"{BASE_URL}/api/users/login", json=data)
    assert response.status_code == 400
    assert response.text == "Invalid identifier format"