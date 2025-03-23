Feature: User Update API

  Background:
    Given an existing user with the following details:
      | id   | name | email       | phoneNumber | password     | countryCode | address  |
      | 589  | time | financial   | 1234567890  | @yLh(Zdui6z  | IN          | anything |

  Scenario: Successfully update user information
    Given I am authenticated with a valid Bearer token
    When I send a POST request to "/api/users/update" with the following JSON payload:
      """
      {
        "id": 589,
        "name": "newName",
        "email": "newemail@example.com",
        "phoneNumber": "1234567899",
        "password": "@yLh(Zdui6z",
        "countryCode": "IN",
        "address": "new address"
      }
      """
    Then the response status code should be 200
    And the response body should indicate success

  Scenario: Update user with existing email
    Given I am authenticated with a valid Bearer token
    And an existing user with email "financial" exists
    When I send a POST request to "/api/users/update" with JSON payload where email is "financial"
    Then the response status code should be 400
    And the response body should be a simple string 
    And the response should indicate "Email already exists"

  Scenario: Update user with duplicate phone number
    Given I am authenticated with a valid Bearer token
    And an existing user with phone number "single" exists
    When I send a POST request to "/api/users/update" with JSON payload where phoneNumber is "single"
    Then the response status code should be 400
    And the response body should indicate "Phone number already exists"

  Scenario: Update user with invalid phone number length
    Given I am authenticated with a valid Bearer token
    When I send a POST request to "/api/users/update" with a JSON payload where phoneNumber length is less than 10
    Then the response status code should be 400

  Scenario: Update user with invalid password policy
    Given I am authenticated with a valid Bearer token
    When I send a POST request to "/api/users/update" with a JSON payload where password does not meet policy criteria
    Then the response status code should be 400