Feature: Cash Withdrawal

  Background:
    Given a user with account number "856899" has logged in with identifier "genai_test_user@example.com" and password "Secure#1234"
    And a valid bearer token has been generated

  Scenario: Successful cash withdrawal
    Given the account balance is sufficient
    When the user withdraws an amount of 400 from their account
    Then the withdrawal should be successful
    And the response should have a status code of 200

  Scenario: Withdrawal with insufficient funds
    Given the account balance is less than the requested amount
    When the user tries to withdraw an amount of 5000
    Then the withdrawal should be denied
    And the response should indicate insufficient funds

  Scenario: Withdrawal amount is not a multiple of 100
    When the user tries to withdraw an amount of 411.06
    Then the withdrawal should be denied
    And the response should indicate that the amount must be in multiples of 100

  Scenario: Invalid PIN number
    When the user tries to withdraw an amount of 400 with an incorrect pin "0000"
    Then the withdrawal should be denied
    And the response should indicate an invalid PIN

  Scenario: Unauthorized withdrawal attempt
    Given the user does not have a valid bearer token
    When the user tries to withdraw an amount of 400
    Then the withdrawal should be denied
    And the response should have a status code of 401

  Scenario: Withdrawal with the amount exceeding the maximum allowable limit
    Given the account balance is sufficient
    When the user tries to withdraw an amount of 150000
    Then the withdrawal should be denied
    And the response should indicate an invalid amount
