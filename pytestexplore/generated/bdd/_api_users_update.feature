Feature: User Update API

  Scenario: Successful user profile update
    Given a user with ID 679 exists
    And I have a valid Bearer token
    When I send a PATCH request to "/api/users/update" with the following data:
      | id          | name      | password    | email         | countryCode | phoneNumber | address      |
      | 679         | increase  | Fu%0Pny5HR  | administration| explain     | myself      | easy         |
    Then the response status code should be 200
    And the response should indicate a successful update

  Scenario: Unauthorized access without Bearer token
    Given a user with ID 679 exists
    When I send a PATCH request to "/api/users/update" without a Bearer token
    Then the response status code should be 401
    And the response should indicate an authentication failure

  Scenario: Update with invalid email
    Given a user with ID 679 exists
    And I have a valid Bearer token
    When I send a PATCH request to "/api/users/update" with the following invalid email data:
      | id          | name      | password    | email         | countryCode | phoneNumber | address      |
      | 679         | increase  | Fu%0Pny5HR  | invalid-email | explain     | myself      | easy         |
    Then the response status code should be 400
    And the response should indicate an email validation failure

  Scenario: Update with existing email
    Given a user with ID 680 exists with email "administration"
    And I have a valid Bearer token
    When I send a PATCH request to "/api/users/update" with the following data:
      | id          | name      | password    | email         | countryCode | phoneNumber | address      |
      | 679         | increase  | Fu%0Pny5HR  | administration| explain     | myself      | easy         |
    Then the response status code should be 400
    And the response should indicate that email already exists

  Scenario: Update with missing required fields
    Given a user with ID 679 exists
    And I have a valid Bearer token
    When I send a PATCH request to "/api/users/update" with missing required fields
    Then the response status code should be 400
    And the response should indicate field validation errors
