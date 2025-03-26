Feature: Fund Transfer API

  Scenario: Successful fund transfer
    Given a user is logged in with token "Bearer <valid-token>"
    And the user has a source account number "fall"
    And the user wants to transfer a valid multiple of 100 amount "500" to target account number "enough"
    And the PIN entered is "1234"
    When the user performs a fund transfer
    Then the fund transfer is successful

  Scenario: Insufficient funds for transfer
    Given a user is logged in with token "Bearer <valid-token>"
    And the user attempts to transfer an amount exceeding the source account balance
    When the user performs a fund transfer
    Then the fund transfer fails with an error message "Insufficient funds"

  Scenario: Invalid PIN for fund transfer
    Given a user is logged in with token "Bearer <valid-token>"
    And the user enters an incorrect PIN "0000"
    When the user attempts to perform a fund transfer
    Then the fund transfer fails with an error message "Invalid PIN"

  Scenario: Invalid authentication token
    Given a user is attempting to perform a fund transfer
    And the token provided is "Bearer <invalid-token>"
    When the fund transfer is attempted
    Then the API returns a 401 error message

  Scenario: Transfer amount not a multiple of 100
    Given a user is logged in with token "Bearer <valid-token>"
    And the user attempts to transfer an amount "568.62" not in multiples of 100
    When the user attempts the fund transfer
    Then the fund transfer fails with a validation error message

  Scenario: Transfer to the same account
    Given a user is logged in with token "Bearer <valid-token>"
    And the user attempts to transfer funds from account number "fall" to the same account "fall"
    When the user attempts the fund transfer
    Then the fund transfer fails with a validation error message "Transfer to the same account is not permitted"