import pytest
from pytest_bdd import scenarios, given, when, then
from playwright.sync_api import sync_playwright
from utils import (
    go_to_page, click_button, wait_for_selector,upload_file, check_email_in_folder,
    check_element_text, check_iframe_text, user_login, new_email
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
FILE_NAME = 'attachment.jpg'
SENT_URL = 'https://roundcube.m1.websupport.sk/?_task=mail&_mbox=Sent'

scenarios('../features/send_email.feature')

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

@given('attachment is uploaded')
def attach_file(page):
    upload_file(page, ATTACHMENT_PATH)
    delete_btn = page.wait_for_selector('ul#attachment-list li a.delete', timeout=5000)
    assert delete_btn.is_visible()

@when('email is sent')
def click_send(page):
    click_button(page, '#rcmbtn114')

@then('email is in inbox and sent folder')
def email_in_folder(page):
    check_email_in_folder(page, SUBJECT_TEXT)
    go_to_page(page, SENT_URL)
    assert page.url == SENT_URL
    check_email_in_folder(page, SUBJECT_TEXT)

@then('email has expected values')
def email_attributes(page):
	go_to_page(page, SENT_URL)
	assert page.url == SENT_URL
	selector = f'td.subject span:has-text("{SUBJECT_TEXT}")'
	click_button(page, selector)
	wait_for_selector(page, '#messagecontframe')
	check_iframe_text(page, 'messagecontframe', '.rcmBody', MESSAGE_BODY)
	check_iframe_text(page, 'messagecontframe', '.attachment-name', ATTACHMENT_PATH.split('/')[-1])

