import pytest
from pytest_bdd import scenarios, given, when, then
from playwright.sync_api import sync_playwright
from utils import (
    click_button, wait_for_selector, upload_file, check_email_in_folder, user_login, new_email
)

# Global parameters
LOGIN_URL = 'https://mail.websupport.sk/'
USERNAME = 'nikolasmrekova@boringcompany.sk'
# ADD YOUR PASSWORD
PASSWORD = ''
DASHBOARD_URL = 'https://roundcube.m1.websupport.sk/?_task=mail&_mbox=INBOX'
CONTACT_NAME = 'Nikola Smrekova'
SUBJECT_TEXT = 'Yoda wants to meet'
MESSAGE_BODY = 'Dear Little Padawan, I miss our time spent together.'
ATTACHMENT_PATH = '../assets/attachment.jpg'

scenarios('../features/insert_attachment.feature')

@pytest.fixture(scope="module")
def playwright_context():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        yield context
        context.close()
        browser.close()

@pytest.fixture
def page(playwright_context):
    return playwright_context.new_page()

@given('user is logged into the email client')
def login(page):
	user_login(page, LOGIN_URL, USERNAME, PASSWORD, DASHBOARD_URL)

@given('new message is created')
def create_new_email(page):
    new_email(page, CONTACT_NAME, SUBJECT_TEXT, MESSAGE_BODY)

@when('attachment is uploaded')
def attach_file(page):
    upload_file(page, ATTACHMENT_PATH)

@then('attachment remove button is visible')
def remove_button_visible(page):
    delete_btn = page.wait_for_selector('ul#attachment-list li a.delete', timeout=5000)
    assert delete_btn.is_visible()

@then('uploaded file name matches selected file name')
def file_name_match(page):
    attachment_name_element = page.locator('ul#attachment-list li a span.attachment-name')
    attachment_name = attachment_name_element.inner_text()
    assert attachment_name in ATTACHMENT_PATH
