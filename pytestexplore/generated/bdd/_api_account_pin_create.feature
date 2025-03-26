Feature: Create PIN for Account

  Background:
    Given the endpoint "/api/account/pin/create" is available
    And a valid Bearer token is obtained using identifier "genai_test_user@example.com" and password "Secure#1234"

  Scenario: Successfully create a new PIN for an account
    Given a valid JSON request payload with accountNumber "856899", pin "1234", and password "Secure#1234"
    When a POST request is made to "/api/account/pin/create" with the payload and Bearer token
    Then the response status code should be 200
    And the response should indicate success

  Scenario: Fail to create PIN with invalid Bearer token
    Given a valid JSON request payload with accountNumber "856899", pin "1234", and password "Secure#1234"
    And an invalid Bearer token
    When a POST request is made to "/api/account/pin/create" with the payload and invalid token
    Then the response status code should be 401
    And the response should indicate authentication failure

  Scenario: Fail to create PIN with duplicate accountNumber and PIN
    Given a valid JSON request payload with accountNumber "856899", pin "1234", and password "Secure#1234"
    And a successful PIN creation request has already been performed
    When a POST request is made to "/api/account/pin/create" with the same payload and Bearer token
    Then the response status code should not be 200
    And the response should indicate failure due to duplicate PIN creation

  Scenario: Fail to create PIN with missing required fields
    Given an invalid JSON request payload missing "pin"
    When a POST request is made to "/api/account/pin/create" with the invalid payload and Bearer token
    Then the response status code should be 400
    And the response should indicate missing required fields