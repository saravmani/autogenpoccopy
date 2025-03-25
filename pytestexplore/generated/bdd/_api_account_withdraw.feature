Feature: Cash Withdrawal

  Scenario: Successful withdrawal
    Given an account with accountNumber "123456" and pin "owner" with sufficient balance
    When the client submits a withdrawal request with accountNumber "123456", pin "owner", and amount 267.67
    Then the response should indicate success

  Scenario: Withdrawal with insufficient balance
    Given an account with accountNumber "123456" and pin "owner" with insufficient balance
    When the client submits a withdrawal request with accountNumber "123456", pin "owner", and amount 267.67
    Then the response should indicate failure due to insufficient funds

  Scenario: Withdrawal with invalid account number
    Given an invalid account number
    When the client submits a withdrawal request with accountNumber "invalid", pin "owner", and amount 267.67
    Then the response should indicate failure due to invalid account number

  Scenario: Withdrawal with incorrect PIN
    Given an account with accountNumber "123456" and pin "wrong"
    When the client submits a withdrawal request with accountNumber "123456", pin "wrong", and amount 100
    Then the response should indicate failure due to incorrect PIN

  Scenario: Duplicate withdrawal request
    Given a successful withdrawal request has been made with accountNumber "123456", pin "owner", and amount 267.67
    When the client tries to repeat the same withdrawal request
    Then the response should indicate a duplicate request warning

  Scenario: Unauthorized access due to missing token
    Given a withdrawal request without a bearer token
    When the client submits a withdrawal request with accountNumber "123456", pin "owner", and amount 100
    Then the response should indicate a failure due to unauthorized access