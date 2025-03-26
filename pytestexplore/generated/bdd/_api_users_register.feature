Feature: User Registration

  Scenario: Successfully registering a new user with valid input
    Given the API endpoint "/api/users/register"
    When I send a POST request with JSON body
      | name        | password     | email                   | countryCode | phoneNumber | address             |
      | John Doe    | Pass#1234567 | john.doe@example.com    | IN          | 1234567890  | 123 Elm Street, NYC |
    Then the API response status code should be 200
    And the response should include the user details except password
    And the response should have additional keys "accountNumber", "ifscCode", "branch", "accountType"

  Scenario: Duplicate email registration attempt
    Given the API endpoint "/api/users/register"
    When I send a POST request with JSON body
      | name        | password     | email                   | countryCode | phoneNumber | address             |
      | Jane Doe    | Pass#1234567 | john.doe@example.com    | IN          | 1234567891  | 456 Oak Street, LA  |
    Then the API response should be the error message "Email already exists"

  Scenario: Duplicate phone number registration attempt
    Given the API endpoint "/api/users/register"
    When I send a POST request with JSON body
      | name        | password     | email                   | countryCode | phoneNumber | address             |
      | Jane Smith  | Pass#1234567 | jane.smith@example.com  | IN          | 1234567890  | 789 Pine Street, SF |
    Then the API response should be the error message "Phone number already exists"

  Scenario: Registration attempt with invalid password
    Given the API endpoint "/api/users/register"
    When I send a POST request with JSON body
      | name        | password | email                   | countryCode | phoneNumber | address                 |
      | Bob Brown   | pass123  | bob.brown@example.com   | IN          | 9876543210  | 321 Maple Street, DC   |
    Then the API response status code should be 400

  Scenario: Registration attempt with missing required fields
    Given the API endpoint "/api/users/register"
    When I send a POST request with incomplete JSON body
      | name        | password     | email                   | countryCode | phoneNumber | address             |
      | missingName | Pass#1234567 | myemail@example.com     | IN          | 1230984567  |                     |
    Then the API response status code should be 400