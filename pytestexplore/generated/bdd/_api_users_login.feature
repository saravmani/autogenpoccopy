Feature: User Login

  Scenario: Successful login with valid credentials
    Given the API endpoint "/api/users/login" is available
    When I send a POST request with valid identifier "daughter" and password "Hx%4L7sy*M"
    Then I should receive a 200 OK status code
    And the response should contain an authentication token

  Scenario: Unsuccessful login with invalid credentials
    Given the API endpoint "/api/users/login" is available
    When I send a POST request with identifier "daughter" and incorrect password "wrongPassword123!"
    Then I should receive a 401 Unauthorized status code
    And an error message "Invalid credentials" should be returned

  Scenario: Unsuccessful login with missing password
    Given the API endpoint "/api/users/login" is available
    When I send a POST request with identifier "daughter" and no password
    Then I should receive a 400 Bad Request status code
    And an error message "Password is required" should be returned

  Scenario: Unsuccessful login with missing identifier
    Given the API endpoint "/api/users/login" is available
    When I send a POST request with no identifier and password "Hx%4L7sy*M"
    Then I should receive a 400 Bad Request status code
    And an error message "Identifier is required" should be returned

  Scenario: Unsuccessful login with invalid identifier type
    Given the API endpoint "/api/users/login" is available
    When I send a POST request with identifier as number 123456 and password "Hx%4L7sy*M"
    Then I should receive a 400 Bad Request status code
    And an error message "Invalid identifier format" should be returned
