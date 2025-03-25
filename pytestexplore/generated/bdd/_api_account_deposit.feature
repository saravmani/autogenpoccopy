Feature: Cash Deposit 

  Scenario: Successfully deposit cash into an account
    Given the account exists with accountNumber "1234567890" and pin "1234"
    And a valid authentication token is provided
    When a deposit of amount 195.94 is made to the account
    Then the deposit should be successful
    And a success message should be returned

  Scenario: Deposit with invalid account number
    Given an invalid accountNumber "9999999999"
    And a valid authentication token is provided
    When a deposit of amount 200.00 is attempted
    Then the deposit should fail
    And an error message should be returned

  Scenario: Deposit with incorrect pin
    Given the account exists with accountNumber "1234567890"
    And an incorrect pin "0000" is provided
    And a valid authentication token is provided
    When a deposit of amount 100.00 is attempted
    Then the deposit should fail
    And an error message indicating pin error should be returned

  Scenario: Deposit without authentication token
    Given the account exists with accountNumber "1234567890" and pin "1234"
    When a deposit of amount 150.00 is made without an authentication token
    Then the deposit should fail
    And an authentication error message should be returned

  Scenario: Deposit with invalid amount format
    Given the account exists with accountNumber "1234567890" and pin "1234"
    And a valid authentication token is provided
    When a deposit with invalid amount format "ABC" is made
    Then the deposit should fail
    And an error message for invalid amount should be returned
