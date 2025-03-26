Feature: Cash Deposit to an Account

  Background:
    Given the user is logged in with identifier "genai_test_user@example.com" and password "Secure#1234"
    And has a valid bearer token

  Scenario: Successful cash deposit with a valid amount
    Given the account number is "856899"
    And the PIN is "1234"
    And the deposit amount is "500"
    When the user deposits money to the account
    Then the response status code should be 200

  Scenario: Deposit fails due to amount greater than 100,000
    Given the account number is "856899"
    And the PIN is "1234"
    And the deposit amount is "100500"
    When the user deposits money to the account
    Then the response status code should not be 200

  Scenario: Deposit fails due to invalid amount not in multiples of 100
    Given the account number is "856899"
    And the PIN is "1234"
    And the deposit amount is "527"
    When the user deposits money to the account
    Then the response status code should not be 200

  Scenario: Deposit fails due to amount less than or equal to 0
    Given the account number is "856899"
    And the PIN is "1234"
    And the deposit amount is "0"
    When the user deposits money to the account
    Then the response status code should not be 200

  Scenario: Deposit fails due to invalid authentication token
    Given the user is logged in with an invalid token
    And the account number is "856899"
    And the PIN is "1234"
    And the deposit amount is "500"
    When the user attempts to deposit money
    Then the response status code should be 401