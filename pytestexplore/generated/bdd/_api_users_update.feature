Feature: User Update API

  Background:
    Given a user exists with the following details:
      | id    | name   | password   | email                    | countryCode | phoneNumber | address        |
      | 759   | little | Kyz905AzO$ | data                     | medical     | sea         | environment    |
    And the user is authenticated with a valid Bearer token

  Scenario: Successfully update user details
    Given the current user information is:
      | id    | name   | password   | email                    | countryCode | phoneNumber | address        |
      | 759   | little | Kyz905AzO$ | data                     | medical     | sea         | environment    |
    When the user sends a POST request to "/api/users/update" with the new details:
      | id    | name       | email            | countryCode | phoneNumber | address         |
      | 759   | updatedName| updatedEmail     | newCountry  | newPhone    | newEnvironment  |
    Then the response should indicate a successful update with status code 200

  Scenario: Attempt to update user details with invalid token
    Given the current user information is:
      | id    | name   | password   | email                    | countryCode | phoneNumber | address        |
      | 759   | little | Kyz905AzO$ | data                     | medical     | sea         | environment    |
    And the user provides an invalid Bearer token
    When the user sends a POST request to "/api/users/update" with any new details:
      | id    | name       | email            | countryCode | phoneNumber |
      | 759   | updatedName| updatedEmail     | newCountry  | newPhone    |
    Then the response should indicate failure due to authentication error with status code 401

  Scenario: Attempt to update user details with missing required fields
    Given the current user information is:
      | id    | name   | password   | email                    | countryCode | phoneNumber | address        |
      | 759   | little | Kyz905AzO$ | data                     | medical     | sea         | environment    |
    When the user sends a POST request to "/api/users/update" missing required email field:
      | id    | name       | email | countryCode | phoneNumber | address         |
      | 759   | updatedName|       | newCountry  | newPhone    | newEnvironment  |
    Then the response should indicate failure due to missing fields with status code 400
