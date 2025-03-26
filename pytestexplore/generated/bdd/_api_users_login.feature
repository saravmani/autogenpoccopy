Feature: User Login API

  Background:
    Given a user with identifier "genai_test_user@example.com" and password "Secure#1234"

  Scenario: Successful login
    When the user attempts to login with identifier "genai_test_user@example.com" and password "Secure#1234"
    Then the response status code should be 200
    And the response should contain a token

  Scenario: Login with incorrect password
    When the user attempts to login with identifier "genai_test_user@example.com" and password "wrong_password"
    Then the response status code should be 401
    And the response should contain an error message indicating invalid credentials

  Scenario: Login with incorrect identifier
    When the user attempts to login with identifier "wrong_user@example.com" and password "Secure#1234"
    Then the response status code should be 401
    And the response should contain an error message indicating invalid credentials

  Scenario: Login with missing identifier
    When the user attempts to login with empty identifier and password "Secure#1234"
    Then the response status code should be 400
    And the response should contain an error message indicating missing identifier

  Scenario: Login with missing password
    When the user attempts to login with identifier "genai_test_user@example.com" and empty password
    Then the response status code should be 400
    And the response should contain an error message indicating missing password