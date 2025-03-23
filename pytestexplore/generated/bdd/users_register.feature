Feature: User Registration for Banking Portal

  Background:
    Given the user registration endpoint is "/api/users/register"

  Scenario: Successful user registration
    Given a new user with the following details
      | name       | password      | email                | countryCode | phoneNumber | address             |
      | John Doe   | Password$123  | johndoe@example.com  | IN          | 1234567890  | 123 Baker Street    |
    When the user submits the registration form
    Then the registration should be successful
    And the response status code should be 200
    And the response should contain the user's information except the password

  Scenario: Registration with duplicate email
    Given an existing user with the email "duplicate@example.com"
    And a new user with the following details
      | name        | password      | email                | countryCode | phoneNumber | address          |
      | Jane Doe    | Password$123  | duplicate@example.com | IN          | 0987654321  | 456 Elm Street   |
    When the user submits the registration form
    Then the registration should fail
    And the response status code should be 400
    And the response should be "Email already exists"

  Scenario: Registration with duplicate phone number
    Given an existing user with the phone number "1234567890"
    And a new user with the following details
      | name        | password      | email                 | countryCode | phoneNumber | address          |
      | Alice Smith | Password$123  | alice@example.com     | IN          | 1234567890  | 789 Pine Avenue  |
    When the user submits the registration form
    Then the registration should fail
    And the response status code should be 400
    And the response should be "Phone number already exists"

  Scenario: Registration with invalid password
    Given a new user with the following details
      | name      | password   | email                | countryCode | phoneNumber | address             |
      | Bob Jones | weakpass   | bob@example.com     | IN          | 2233445566  | 321 Oak Lane        |
    When the user submits the registration form
    Then the registration should fail
    And the response status code should be 400