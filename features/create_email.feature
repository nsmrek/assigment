Feature: Create Email

  Scenario: Create email message for a person from contacts
	Given user is logged into the email client
	When user creates a new email
	And user selects person from my contacts
	And user enters the subject
	And user enters the message
	Then addressee is filled
	And body is filled

