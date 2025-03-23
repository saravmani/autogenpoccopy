Feature: User Registration

  Scenario: Successful registration
    Given a new user with name "reveal", password "#EmHS5Yk21", email "reveal@example.com", countryCode "IN", phoneNumber "1234567890", address "123 Main St, City"
    When the user registers with the banking portal
    Then the response status should be 200
    And the response should contain account details excluding the password

  Scenario: Registration with existing email
    Given an existing user with email "existing@example.com"
    When a new user registers with name "newuser", password "#EmHS5Yk21", email "existing@example.com", countryCode "IN", phoneNumber "0987654321", address "456 Main St, City"
    Then the response should be an error message "Email already exists"
    And the response status should be 400

  Scenario: Registration with existing phone number
    Given an existing user with phoneNumber "1234567890"
    When a new user registers with name "anotheruser", password "#EmHS5Yk21", email "another@example.com", countryCode "IN", phoneNumber "1234567890", address "789 Main St, City"
    Then the response should be an error message "Phone number already exists"
    And the response status should be 400

  Scenario: Registration with invalid phone number length
    When the user registers with name "invalid", password "#EmHS5Yk21", email "invalid@example.com", countryCode "IN", phoneNumber "1234", address "1010 Main St, City"
    Then the response status should be 400

  Scenario: Registration with weak password
    When the user registers with name "weakpassword", password "password", email "weak@example.com", countryCode "IN", phoneNumber "2345678901", address "1020 Main St, City"
    Then the response status should be 400