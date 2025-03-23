import pytest
import requests
from pytest_bdd import scenario, given, when, then, parsers

API_URL = "/api/users/register"

@scenario("dynamictest_test.feature", "Successful User Registration")
def test_successful_registration():
    pass

@scenario("dynamictest_test.feature", "User Registration with Duplicate Phone Number")
def test_duplicate_phone_number():
    pass

@scenario("dynamictest_test.feature", "User Registration with Duplicate Email")
def test_duplicate_email():
    
    pass

@scenario("dynamictest_test.feature", "User Registration with Invalid Password")
def test_invalid_password():
    pass

@given(parsers.parse("the User provides the following registration details:\n{table}"))
def registration_details(table):
    return [
        {
            "name": row["name"],
            "password": row["password"],
            "email": row["email"],
            "countryCode": row["countryCode"],
            "phoneNumber": row["phoneNumber"],
            "address": row["address"],
        }
        for row in table.rows
    ]

@when("the User sends a POST request to the API URL /api/users/register with valid registration details")
def send_valid_registration_request(registration_details):
    response = requests.post(
        API_URL, json=registration_details[0]
    )  # Using the first user's data
    return response

@when("the User sends a POST request to the API URL /api/users/register with an existing phone number")
def send_duplicate_phone_request(registration_details):
    # Assuming registration_details is already populated from the background
    payload = registration_details[1].copy() #using the second users data
    # making the phone number duplicate.
    payload['phoneNumber'] = registration_details[0]['phoneNumber']
    response = requests.post(API_URL, json=payload)
    return response

@when("the User sends a POST request to the API URL /api/users/register with an existing email")
def send_duplicate_email_request(registration_details):
    payload = registration_details[2].copy() #using the third user's data
    # making the email duplicate.
    payload['email'] = registration_details[0]['email']
    response = requests.post(API_URL, json=payload)
    return response

@when("the User sends a POST request to the API URL /api/users/register with an invalid password")
def send_invalid_password_request(registration_details):
    payload = registration_details[0].copy()
    payload['password'] = 'short'  # Invalid password for example
    response = requests.post(API_URL, json=payload)
    return response

@then(parsers.parse("the API should return a {status_code:d} status code"))
def check_status_code(response, status_code):
    assert response.status_code == status_code

@then(parsers.parse("the response should include the following:\n{table}"))
def check_response_body(response, table):
    expected_data = [
        {k: v for k, v in row.items()} for row in table.rows
    ]
    response_data = response.json()
    for expected_item in expected_data:
        for key, value in expected_item.items():
            if "<generated>" not in value:
                assert response_data[key] == value

@then(parsers.parse('the response message should be "{message}"'))
def check_error_message(response, message):
    assert response.json()["message"] == message