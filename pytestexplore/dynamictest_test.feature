Feature: User Registration API - /api/users/register

  Background:
    Given the User provides the following registration details:
      | name        | password   | email                     | countryCode | phoneNumber   | address                        |
      | Test User 1 | Test@12345 | test_user1@example.com     | IN          | 9876543210   | 123 Test Street, Test City     # Unique details
      | Test User 2 | Test@12345 | test_user2@example.com     | IN          | 9876543211   | 456 Example Road, Example City  # Unique details
      | Test User 3 | Test@12345 | test_user3@example.com     | IN          | 9876543212   | 789 Sample Avenue, Sample City  # Unique details

  Scenario: Successful User Registration
    When the User sends a POST request to the API URL /api/users/register with valid registration details
    Then the API should return a 200 status code
    And the response should include the following:
      | name        | email                     | countryCode | phoneNumber   | address                        | accountNumber | ifscCode   | branch  | accountType |
      | Test User 1 | test_user1@example.com     | IN          | 9876543210   | 123 Test Street, Test City     | <generated>   | <generated> | <generated> | Savings     |
    Then the API should return a 200 status code
    And the response should include the following:
      | name        | email                     | countryCode | phoneNumber   | address                        | accountNumber | ifscCode   | branch  | accountType |
      | Test User 1 | test_user1@example.com     | IN          | 9876543210   | 123 Test Street, Test City     | <generated>   | <generated> | <generated> | Savings     |
    And the response should include the following:
      | name        | email                     | countryCode | phoneNumber   | address                        | accountNumber | ifscCode   | branch  | accountType |
      | Test User 1 | test_user1@example.com     | IN          | 9876543210   | 123 Test Street, Test City     | <generated>   | <generated> | <generated> | Savings     |
      | name        | email                     | countryCode | phoneNumber   | address                        | accountNumber | ifscCode   | branch  | accountType |
      | Test User 1 | test_user1@example.com     | IN          | 9876543210   | 123 Test Street, Test City     | <generated>   | <generated> | <generated> | Savings     |
      | Test User 1 | test_user1@example.com     | IN          | 9876543210   | 123 Test Street, Test City     | <generated>   | <generated> | <generated> | Savings     |

  Scenario: User Registration with Duplicate Phone Number
    When the User sends a POST request to the API URL /api/users/register with an existing phone number
    Then the API should return a 400 Bad Request error
    And the response message should be "Phone number already exists"

  Scenario: User Registration with Duplicate Email
    When the User sends a POST request to the API URL /api/users/register with an existing email
    Then the API should return a 400 Bad Request error
    And the response message should be "Email already exists"

  Scenario: User Registration with Invalid Password
    When the User sends a POST request to the API URL /api/users/register with an invalid password
    Then the API should return a 400 Bad Request error
    And the response message should specify the password requirements