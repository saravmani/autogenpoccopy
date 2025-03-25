Feature: Fund Transfer

  Scenario: Successful fund transfer
    Given a user is authenticated with a valid bearer token
    And the user has sufficient balance in the source account
    When the user initiates a fund transfer with
      | sourceAccountNumber | team       |
      | targetAccountNumber | everything |
      | amount              | 966.27     |
      | pin                 | partner    |
    Then the fund transfer is successful
    And a success message is returned

  Scenario: Fund transfer with insufficient balance
    Given a user is authenticated with a valid bearer token
    And the user has insufficient balance in the source account
    When the user initiates a fund transfer with
      | sourceAccountNumber | team       |
      | targetAccountNumber | everything |
      | amount              | 966.27     |
      | pin                 | partner    |
    Then the fund transfer should fail
    And an appropriate error message is returned

  Scenario: Fund transfer with invalid pin
    Given a user is authenticated with a valid bearer token
    When the user initiates a fund transfer with
      | sourceAccountNumber | team       |
      | targetAccountNumber | everything |
      | amount              | 966.27     |
      | pin                 | wrongPin   |
    Then the fund transfer should fail
    And an invalid pin error message is returned

  Scenario: Fund transfer to non-existing target account
    Given a user is authenticated with a valid bearer token
    When the user initiates a fund transfer with
      | sourceAccountNumber | team       |
      | targetAccountNumber | nonExist   |
      | amount              | 966.27     |
      | pin                 | partner    |
    Then the fund transfer should fail
    And a target account not found error message is returned
