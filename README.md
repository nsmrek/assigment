Email Client Testing
In the assignment I cover following 5 test scenarios, I used playwright and pytest-BDD and for test description gherkin:
1. User Login
    * Scenario: User accesses the login page, enter valid credentials, and are redirected to the dashboard upon successful login.
2. Create Email
    * Scenario: User logs in, create a new email, select a contact, enter subject and message, ensuring fields are populated correctly.
3. Insert Attachment
    * Scenario: User logs in, creates a new email, upload an attachment, verify attachment visibility and correctness of uploaded file name.
4. Send Email
    * Scenario: User logs in, composes an email with an attachment, send it, and ensure it appears correctly in both inbox and sent folders with expected content.
5. User Logout
    * Scenario: User logs into the email client initiate logout, resulting in redirection to the login page, effectively ending the session.
