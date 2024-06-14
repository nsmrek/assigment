import pytest
from pytest_bdd import scenarios, given, when, then
from playwright.sync_api import sync_playwright
from utils import go_to_page, fill_credentials, click_button, wait_for_selector, get_element_text, user_login

# Global parameters
LOGIN_URL = 'https://mail.websupport.sk/'
USERNAME = 'nikolasmrekova@boringcompany.sk'
# ADD YOUR PASSWORD
PASSWORD = ''
DASHBOARD_URL = 'https://roundcube.m1.websupport.sk/?_task=mail&_mbox=INBOX'
LOGOUT_URL = 'https://mail.websupport.sk/#logout'

scenarios('../features/user_logout.feature')

@pytest.fixture(scope="module")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()

@pytest.fixture
def page(browser):
    page = browser.new_page()
    yield page
    page.close()

@given('user is logged into the email client')
def login(page):
	user_login(page, LOGIN_URL, USERNAME, PASSWORD, DASHBOARD_URL)

@when('user clicks logout button')
def logout(page):
    click_button(page, '#rcmbtn112')

@then('user is redirected to login page')
def check_logout(page):
    wait_for_selector(page, '#ws-webmail-login')
    assert page.url == LOGOUT_URL
