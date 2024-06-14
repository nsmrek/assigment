Feature: User Logout

  Scenario: Successful logout from email client
	Given user is logged into the email client
	When user clicks logout button
	Then user is redirected to login page
