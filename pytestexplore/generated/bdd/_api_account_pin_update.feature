Feature: Update PIN

  Scenario: Successfully update the PIN
    Given I have a valid authentication token
    And I have an account with accountNumber "856899"
    And my current PIN is "1234"
    And I know my account password "Secure#1234"
    When I send a POST request to "/api/account/pin/update" with the oldPin "1234", newPin "5678", accountNumber "856899", and password "Secure#1234"
    Then the response status code should be 200
    And the response message should indicate a successful PIN update

  Scenario: Fail to update PIN due to incorrect old PIN
    Given I have a valid authentication token
    And I have an account with accountNumber "856899"
    And my current PIN is "1234"
    And I know my account password "Secure#1234"
    When I send a POST request to "/api/account/pin/update" with the oldPin "1111", newPin "5678", accountNumber "856899", and password "Secure#1234"
    Then the response status code should be 403
    And the response message should indicate incorrect old PIN

  Scenario: Fail to update PIN due to missing authentication token
    Given I have an account with accountNumber "856899"
    And my current PIN is "1234"
    And I know my account password "Secure#1234"
    When I send a POST request to "/api/account/pin/update" without an authentication token
    Then the response status code should be 401
    And the response message should indicate authentication failure

  Scenario: Fail to update PIN due to weak new PIN
    Given I have a valid authentication token
    And I have an account with accountNumber "856899"
    And my current PIN is "1234"
    And I know my account password "Secure#1234"
    When I send a POST request to "/api/account/pin/update" with the oldPin "1234", newPin "12", accountNumber "856899", and password "Secure#1234"
    Then the response status code should be 400
    And the response message should indicate weak new PIN

  Scenario: Fail to update PIN due to incorrect password
    Given I have a valid authentication token
    And I have an account with accountNumber "856899"
    And my current PIN is "1234"
    When I send a POST request to "/api/account/pin/update" with the oldPin "1234", newPin "5678", accountNumber "856899", and password "WrongPassword123"
    Then the response status code should be 403
    And the response message should indicate incorrect password
