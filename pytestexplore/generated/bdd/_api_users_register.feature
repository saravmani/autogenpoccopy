Feature: User Registration

  Scenario: Successfully register a new user
    Given I have user details with name "John Doe", password "Secure#1234", email "john.doe@example.com", country code "IN", phone number "9876543210", address "123 Main St, New Delhi"
    When I POST the user registration details to "/api/users/register"
    Then the response status should be 200
    And the response should contain the user's name, email, country code "IN", phone number "9876543210", address, and account details

  Scenario: Register user with duplicate phone number
    Given a user already exists with phone number "9876543210"
    And I have user details with name "Jane Doe", password "AnotherSecure#1234", email "jane.doe@example.com", country code "IN", phone number "9876543210", address "456 Second St, Mumbai"
    When I POST the user registration details to "/api/users/register"
    Then the response status should be 400
    And the response should be the error message "Phone number already exists"

  Scenario: Register user with duplicate email
    Given a user already exists with email "jane.doe@example.com"
    And I have user details with name "Jim Doe", password "GoodPass#5678", email "jane.doe@example.com", country code "IN", phone number "9876543219", address "789 Third St, Chennai"
    When I POST the user registration details to "/api/users/register"
    Then the response status should be 400
    And the response should be the error message "Email already exists"

  Scenario: Register user with invalid password
    Given I have user details with name "Jake Doe", password "simplepass", email "jake.doe@example.com", country code "IN", phone number "9876543220", address "101 First St, Kolkata"
    When I POST the user registration details to "/api/users/register"
    Then the response status should be 400

  Scenario: Register user with invalid phone number length
    Given I have user details with name "Lara Doe", password "Complex#1234", email "lara.doe@example.com", country code "IN", phone number "98765", address "303 Fourth St, Bangalore"
    When I POST the user registration details to "/api/users/register"
    Then the response status should be 400
