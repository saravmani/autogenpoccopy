Feature: Password Reset

  Background:
    Given a user with email "genai_test_user@example.com" and password "Secure#1234"
    
  Scenario: Successfully reset the password
    Given I have access to the password reset API
    When I provide the identifier as "prevent" and new password as "x73TrJMp_!"
    Then the response should be a success message indicating password reset

  Scenario: Missing identifier
    Given I have access to the password reset API
    When I provide no identifier and new password as "x73TrJMp_!"
    Then the response should indicate a failure due to missing identifier

  Scenario: Missing new password
    Given I have access to the password reset API
    When I provide the identifier as "prevent" and no new password
    Then the response should indicate a failure due to missing new password

  Scenario: New password does not meet policy
    Given I have access to the password reset API
    When I provide the identifier as "prevent" and new password as "short"
    Then the response should indicate a failure due to password policy not being met

  Scenario: Reset password with non-existing identifier
    Given I have access to the password reset API
    When I provide a non-existing identifier as "nonexistent@example.com" and new password as "x73TrJMp_!"
    Then the response should indicate a failure due to non-existing user identifier
