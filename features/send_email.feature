Feature: Send Email

  Scenario: Send email with attachment
	Given user is logged into the email client
	And new message is created
	And attachment is uploaded
	When email is sent
	Then email is in inbox and sent folder
	And email has expected values
