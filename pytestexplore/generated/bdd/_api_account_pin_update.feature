Feature: Update Account PIN

  Background:
    Given the API requires bearer token authentication
    And a valid bearer token is "validBearerToken"

  Scenario: Successfully update account PIN
    Given a user with account number "thousand" and valid old PIN "relate"
    And valid new PIN "remain" and correct password "mWM8^WXpk!"
    When the user updates the account PIN via "/api/account/pin/update"
    Then the response should indicate a successful PIN update

  Scenario: Update account PIN with incorrect old PIN
    Given a user with account number "thousand"
    And incorrect old PIN "incorrectPin"
    When the user attempts to update the account PIN with new PIN "remain"
    Then the response should indicate a failure due to incorrect old PIN

  Scenario: Update account PIN with unauthorized access
    Given a user without a valid bearer token
    When the user attempts to update the account PIN
    Then the response should indicate an unauthorized access error

  Scenario: Update account PIN with invalid new PIN format
    Given a user with account number "thousand" and valid old PIN "relate"
    And invalid new PIN "short"
    When the user attempts to update the account PIN
    Then the response should indicate a failure due to invalid PIN format
