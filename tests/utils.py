from playwright.sync_api import Page

def go_to_page(page: Page, url: str, timeout: int = 5000):
    """
    Navigates to a specified URL.

    Args:
        page (Page): The Playwright page object.
        url (str): The URL to navigate to.
        timeout (int): Maximum time in milliseconds to wait for the page to load. Default is 5000.
    """
    page.goto(url, timeout=timeout)

def fill_credentials(page: Page, username: str, password: str):
    """
    Fills in the login credentials.

    Args:
        page (Page): The Playwright page object.
        username (str): The username to fill in.
        password (str): The password to fill in.
    """
    page.fill('input[name="_user"]', username)
    page.fill('input[name="_pass"]', password)

def click_button(page: Page, selector: str):
    """
    Clicks a button specified by the selector.

    Args:
        page (Page): The Playwright page object.
        selector (str): The selector of the button to click.
    """
    page.click(selector)

def wait_for_selector(page: Page, selector: str, timeout: int = 5000):
    """
    Waits for a selector to appear on the page.

    Args:
        page (Page): The Playwright page object.
        selector (str): The selector to wait for.
        timeout (int): Maximum time in milliseconds to wait for the selector. Default is 5000.
    """
    selector = page.locator(selector)
    selector.wait_for(timeout=timeout)

def get_element_text(page: Page, selector: str) -> str:
    """
    Retrieves the inner text of an element specified by the selector.

    Args:
        page (Page): The Playwright page object.
        selector (str): The selector of the element.

    Returns:
        str: The inner text of the element.
    """
    return page.query_selector(selector).inner_text()

def click_contact(page: Page, contact_name: str):
    """
    Clicks a contact specified by the contact name.

    Args:
        page (Page): The Playwright page object.
        contact_name (str): The name of the contact to click.
    """
    contact_selector = f"text={contact_name}"
    page.click(contact_selector)

def fill_element(page: Page, attribute: str, value: str):
    """
    Fills an element specified by its attribute and value.

    Args:
        page (Page): The Playwright page object.
        attribute (str): The attribute of the element.
        value (str): The value to fill in the element.
    """
    page.fill(f'[{attribute}]', value)

def check_element_text(page: Page, selector: str, expected_text: str):
    """
    Checks if the text of an element matches the expected text.

    Args:
        page (Page): The Playwright page object.
        selector (str): The selector of the element.
        expected_text (str): The expected text to check for.

    Raises:
        AssertionError: If the expected text is not found in the element's text.
    """
    element = page.locator(selector)
    element_text = element.inner_text()
    assert expected_text in element_text, f"Expected text '{expected_text}' not found in element text."

def fill_iframe(page: Page, iframe_id: str, selector: str, value: str):
    """
    Fills an element inside an iframe.

    Args:
        page (Page): The Playwright page object.
        iframe_id (str): The ID of the iframe.
        selector (str): The selector of the element inside the iframe.
        value (str): The value to fill in the element.

    Raises:
        AssertionError: If the iframe with the specified ID is not found.
    """
    iframe = page.frame(name=iframe_id)
    assert iframe is not None, f"Iframe with id '{iframe_id}' not found"
    iframe.fill(selector, value)

def check_iframe_text(page: Page, iframe_id: str, selector: str, expected_text: str):
    """
    Checks if the text of an element inside an iframe matches the expected text.

    Args:
        page (Page): The Playwright page object.
        iframe_id (str): The ID of the iframe.
        selector (str): The selector of the element inside the iframe.
        expected_text (str): The expected text to check for.

    Raises:
        AssertionError: If the expected text is not found in the element's text inside the iframe.
    """
    iframe = page.frame(name=iframe_id)
    element_text = iframe.inner_text(selector)
    assert expected_text in element_text, f"Expected text '{expected_text}' not found in element text."

def check_email_in_folder(page: Page, subject: str) -> bool:
    """
    Checks if an email with the specified subject is present in the folder.

    Args:
        page (Page): The Playwright page object.
        subject (str): The subject of the email to check for.

    Raises:
        AssertionError: If the email with the specified subject is not found.
    """
    selector = f'td.subject span:has-text("{subject}")'
    try:
        page.wait_for_selector(selector, timeout=5000)
        return True
    except Exception as e:
        assert False, f"Email with subject '{subject}' not found in folder. Error: {e}"

def upload_file(page: Page, file_path: str):
    """
    Uploads a file specified by the file path.

    Args:
        page (Page): The Playwright page object.
        file_path (str): The path of the file to upload.
    """
    file_input = page.locator('input#uploadformInput[type="file"][name="_attachments[]"]')
    file_input.set_input_files(file_path, timeout=5000)

def user_login(page: Page, login_url: str, username: str, password: str, dashboard_url: str):
    """
    Logs in the user to a specified dashboard after filling in credentials and clicking login.

    Args:
        page (Page): The Playwright page object.
        login_url (str): The URL of the login page.
        username (str): The username to log in with.
        password (str): The password to log in with.
        dashboard_url (str): The expected URL of the dashboard after successful login.

    Raises:
        AssertionError: If the login process fails or if the user is not redirected to the dashboard URL.
    """
    go_to_page(page, login_url)
    fill_credentials(page, username, password)
    click_button(page, 'button[type="submit"]')
    wait_for_selector(page, '#messagelist')
    assert page.url == dashboard_url, f"Expected dashboard URL '{dashboard_url}', but got '{page.url}'"

def new_email(page: Page, contact_name: str, subject_name: str, message_body: str):
    """
    Creates a new email by filling in recipient, subject, and message body.

    Args:
        page (Page): The Playwright page object.
        contact_name (str): The name of the contact to send the email to.
        subject_name (str): The subject of the email.
        message_body (str): The content of the email message.
    """
    click_button(page, '.compose')
    click_button(page, '.input-group-text.icon.add.recipient')
    click_button(page, 'text=Osobné adresy')
    click_contact(page, contact_name)
    click_button(page, '.mainaction.insert.recipient.btn.btn-primary')
    fill_element(page, 'name="_subject"', subject_name)
    fill_iframe(page, 'composebody_ifr', 'body', message_body)
