Feature: User Login

  Scenario: Successful login with valid credentials
	Given user is on the login page
	When user enters a valid username and password
	And user clicks the login button
	Then user is redirected to the dashboard
