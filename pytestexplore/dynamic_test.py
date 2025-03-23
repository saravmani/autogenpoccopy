import pytest
import requests

BASE_URL = "http://localhost:8080"  # Use the provided BASE_URL from the system message
TOKEN = "Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIwMTdhMjgiLCJpYXQiOjE3NDI2NTcxNTQsImV4cCI6MTc0Mjc0MzU1NH0.3oXrAEV0dnmthYAXQM3dEydNaGzwN8sYyjZu534s3mdU8Lyzqs5lpRQH550VwxY6gT-H3hB5CBBumN99MnIHQg"  # Replace 'your_bearer_token_here' with a valid token
 
 

BASE_URL = "http://localhost:8080"



def test_user_registration_success():
    payload = {
        "name": "Test User",
        "password": "Password123!",
        "email": "testuser@example.com",
        "countryCode": "IN",
        "phoneNumber": "9999999999",
        "address": "123 Test St"
    }
    response = requests.post(f"{BASE_URL}/api/users/register", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["email"] == payload["email"]
    assert data["countryCode"] == payload["countryCode"]
    assert data["phoneNumber"] == payload["phoneNumber"]
    assert data["address"] == payload["address"]