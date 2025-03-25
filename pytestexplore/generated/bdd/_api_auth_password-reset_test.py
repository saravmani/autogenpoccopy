import pytest
import requests

BASE_URL = "http://localhost:8080"

def test_successful_password_reset():
    payload = {
        "identifier": "source",
        "newPassword": "g0LJL)dK(Y"
    }
    response = requests.post(f"{BASE_URL}/api/auth/password-reset", json=payload)
    
    assert response.status_code == 200
    assert "successful password reset" in response.text

def test_reset_password_invalid_identifier():
    payload = {
        "identifier": "invalid_user",
        "newPassword": "g0LJL)dK(Y"
    }
    response = requests.post(f"{BASE_URL}/api/auth/password-reset", json=payload)
    
    assert response.status_code == 400
    assert "identifier not found" in response.text

def test_reset_password_weak_password():
    payload = {
        "identifier": "source",
        "newPassword": "weak"
    }
    response = requests.post(f"{BASE_URL}/api/auth/password-reset", json=payload)
    
    assert response.status_code == 400
    assert "password strength requirement not met" in response.text

def test_reset_password_missing_identifier():
    payload = {
        "newPassword": "g0LJL)dK(Y"
    }
    response = requests.post(f"{BASE_URL}/api/auth/password-reset", json=payload)
    
    assert response.status_code == 400
    assert "missing identifier" in response.text

def test_reset_password_missing_password():
    payload = {
        "identifier": "source"
    }
    response = requests.post(f"{BASE_URL}/api/auth/password-reset", json=payload)
    
    assert response.status_code == 400
    assert "missing password" in response.text