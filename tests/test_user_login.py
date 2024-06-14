import pytest
from pytest_bdd import scenarios, given, when, then
from playwright.sync_api import sync_playwright
from utils import go_to_page, fill_credentials, click_button, wait_for_selector

# Global parameters
LOGIN_URL = 'https://mail.websupport.sk/'
USERNAME = 'nikolasmrekova@boringcompany.sk'
# ADD YOUR PASSWORD
PASSWORD = ''
DASHBOARD_URL = 'https://roundcube.m1.websupport.sk/?_task=mail&_mbox=INBOX'

scenarios('../features/user_login.feature')

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

@given('user is on the login page')
def go_to_login_page(page):
    go_to_page(page, LOGIN_URL)

@when('user enters a valid username and password')
def enter_valid_credentials(page):
    fill_credentials(page, USERNAME, PASSWORD)

@when('user clicks the login button')
def click_login_button(page):
    click_button(page, 'button[type="submit"]')

@then('user is redirected to the dashboard')
def verify_dashboard(page):
    wait_for_selector(page, '#messagelist')
    assert page.url == DASHBOARD_URL
