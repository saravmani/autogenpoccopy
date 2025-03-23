Feature: User Login Authentication

  Background:
    Given the server url is "http://localhost:8080"

  Scenario: Successful User Login
    Given the user provides a valid "identifier" as "require"
    And the user provides a valid "password" as "b960&LRc_O"
    When the user sends a POST request to "/api/users/login"
    Then the response status code should be 200
    And the response should contain a JWT token

  Scenario: Login with Invalid Password
    Given the user provides a valid "identifier" as "require"
    And the user provides an invalid "password" as "wrongPassword"
    When the user sends a POST request to "/api/users/login"
    Then the response status code should not be 200
    And the response should contain an error message

  Scenario: Login with Non-Existing User
    Given the user provides a non-existing "identifier" as "nonexisting@domain.com"
    And the user provides a valid "password" as "b960&LRc_O"
    When the user sends a POST request to "/api/users/login"
    Then the response status code should not be 200
    And the response should contain an error message

  Scenario: Missing Password Field in Request
    Given the user provides a valid "identifier" as "require"
    And the user does not provide a "password"
    When the user sends a POST request to "/api/users/login"
    Then the response status code should be 400
    And the response should contain an error message

  Scenario: Missing Identifier Field in Request
    Given the user does not provide an "identifier"
    And the user provides a valid "password" as "b960&LRc_O"
    When the user sends a POST request to "/api/users/login"
    Then the response status code should be 400
    And the response should contain an error message

  Scenario: Empty Request Body
    Given the user does not provide any input
    When the user sends a POST request to "/api/users/login"
    Then the response status code should be 400
    And the response should contain an error message

  Scenario: Incorrect Content Type
    Given the user provides a valid "identifier" as "require"
    And the user provides a valid "password" as "b960&LRc_O"
    And the Content-Type is set to "text/plain"
    When the user sends a POST request to "/api/users/login"
    Then the response status code should be 415
    And the response should contain an error message