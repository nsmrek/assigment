Feature: Insert Attachment

  Scenario: Create email message with attachment
	Given user is logged into the email client
	And new message is created
	When attachment is uploaded
	Then attachment remove button is visible
	And uploaded file name matches selected file name
