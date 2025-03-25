Feature: Create PIN for Account
  In order to secure my account
  As an account holder
  I want to be able to create a PIN using /api/account/pin/create

  Background:
    Given a valid Bearer token for user authentication

  Scenario: Successfully create a new PIN
    Given I have the following account information
      | accountNumber | pin     | password     |
      | 1234567890    | 1234    | _#61ZRiE#1   |
    When I send a POST request to /api/account/pin/create with this data
    Then I should receive a success message

  Scenario: Fail to create PIN with an existing PIN
    Given I have already created a PIN with accountNumber "1234567890"
    When I attempt to create a PIN again for the same account with the same details
    Then I should receive an error message indicating duplicate PIN creation
  
  Scenario: Fail to create PIN due to invalid password
    Given I have the following account information with invalid password
      | accountNumber | pin     | password |
      | 1234567890    | 1234    | password123 |
    When I send a POST request to /api/account/pin/create with this data
    Then I should receive an error message indicating invalid password

  Scenario: Fail to create PIN due to missing field
    Given I have the following account information
      | accountNumber | pin  | password   |
      | 1234567890    |      | _#61ZRiE#1 |
    When I send a POST request to /api/account/pin/create with this data
    Then I should receive an error message indicating missing pin field
