Feature: Password Reset for Banking Portal API

  Scenario: Successfully reset password
    Given the user provides a valid identifier and a strong new password
    When the user sends a POST request to "/api/auth/password-reset" with the payload:
      """
      {
        "identifier": "source",
        "newPassword": "g0LJL)dK(Y"
      }
      """
    Then the response status should be 200
    And the response message should indicate a successful password reset

  Scenario: Attempt to reset password with an invalid identifier
    Given the user provides an invalid identifier
    When the user sends a POST request to "/api/auth/password-reset" with the payload:
      """
      {
        "identifier": "invalid_user",
        "newPassword": "g0LJL)dK(Y"
      }
      """
    Then the response status should be 400
    And the response message should indicate identifier not found

  Scenario: Attempt to reset password with a weak new password
    Given the user provides a valid identifier and a weak new password
    When the user sends a POST request to "/api/auth/password-reset" with the payload:
      """
      {
        "identifier": "source",
        "newPassword": "weak"
      }
      """
    Then the response status should be 400
    And the response message should indicate password strength requirement not met

  Scenario: Attempting password reset with missing identifier
    Given the user provides a strong new password but no identifier
    When the user sends a POST request to "/api/auth/password-reset" with the payload:
      """
      {
        "newPassword": "g0LJL)dK(Y"
      }
      """
    Then the response status should be 400
    And the response message should indicate missing identifier

  Scenario: Attempting password reset with missing new password
    Given the user provides an identifier but no new password
    When the user sends a POST request to "/api/auth/password-reset" with the payload:
      """
      {
        "identifier": "source"
      }
      """
    Then the response status should be 400
    And the response message should indicate missing password
