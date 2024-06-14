import pytest
from pytest_bdd import scenarios, given, when, then
from playwright.sync_api import sync_playwright
from utils import (
    wait_for_selector, get_element_text, click_button,
    click_contact, fill_element, fill_iframe, upload_file, check_email_in_folder,
    check_element_text, check_iframe_text, user_login
)

# Global parameters
LOGIN_URL = 'https://mail.websupport.sk/'
USERNAME = 'nikolasmrekova@boringcompany.sk'
# ADD YOUR PASSWORD
PASSWORD = ''
CONTACT_NAME = 'Nikola Smrekova'
SUBJECT_TEXT = 'Yoda wants to meet'
MESSAGE_BODY = 'Dear Little Padawan, I miss our time spent together.'
DASHBOARD_URL = 'https://roundcube.m1.websupport.sk/?_task=mail&_mbox=INBOX'

scenarios('../features/create_email.feature')

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

@when('user creates a new email')
def create_new_email(page):
    click_button(page, '.compose')
    wait_for_selector(page, '#compose-content')

@when('user selects person from my contacts')
def select_contact(page):
    click_button(page, '.input-group-text.icon.add.recipient')
    click_button(page, 'text=Osobné adresy')
    click_contact(page, CONTACT_NAME)
    click_button(page, '.mainaction.insert.recipient.btn.btn-primary')

@when('user enters the subject')
def enter_subject(page):
    fill_element(page, 'name="_subject"', SUBJECT_TEXT)

@when('user enters the message')
def enter_message(page):
    fill_iframe(page, 'composebody_ifr', 'body', MESSAGE_BODY)

@then('addressee is filled')
def addressee_filled(page):
    check_element_text(page, '.recipient .name', CONTACT_NAME)

@then('body is filled')
def body_filled(page):
    check_iframe_text(page, 'composebody_ifr', 'body', MESSAGE_BODY)
