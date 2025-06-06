import sys
import contextlib
import signal

from playwright.sync_api import Playwright, sync_playwright

from helpers.helper_functions import log_note, get_random_text, login_nextcloud, close_modal, timeout_handler, user_sleep

DOMAIN = 'https://ncs'

def create_user(playwright: Playwright, browser_name: str, username: str, password: str, email: str) -> None:
    log_note(f"Launch browser {browser_name}")
    if browser_name == "firefox":
        browser = playwright.firefox.launch(headless=False)
    else:
        browser = playwright.chromium.launch(headless=False, args=['--disable-gpu', '--disable-software-rasterizer', '--ozone-platform=wayland'])
    context = browser.new_context(ignore_https_errors=True)
    try:
        page = context.new_page()

        log_note("Opening login page")
        page.goto(f"{DOMAIN}/login")

        log_note("Logging in")
        login_nextcloud(page, domain=DOMAIN)
        user_sleep()

        # Wait for the modal to load. As it seems you can't close it while it is showing the opening animation.
        log_note("Close first-time run popup")
        close_modal(page)

        log_note("Opening create user menu")
        page.click("button[aria-label='Settings menu']")
        page.click("#core_users")
        user_sleep()

        log_note('Adding new user')
        page.get_by_role("button", name="New Account").click()
        page.get_by_placeholder("Account name (required)", exact=True).fill(username)
        page.get_by_placeholder("Password (required)", exact=True).fill(password)
        #page.get_by_placeholder("Email", exact=True).fill(email)
        page.get_by_role("button", name="Add new account").click()
        user_sleep()

        log_note("Close browser")

        # ---------------------
        page.close()
        context.close()
        browser.close()
    except Exception as e:
        if hasattr(e, 'message'): # only Playwright error class has this member
            log_note(f"Exception occurred: {e.message}")

        # set a timeout. Since the call to page.content() is blocking we need to defer it to the OS
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(20)
        #log_note(f"Page content was: {page.content()}")
        signal.alarm(0) # remove timeout signal

        raise e


with sync_playwright() as playwright:
    if len(sys.argv) > 1:
        browser_name = sys.argv[1].lower()
        if browser_name not in ["chromium", "firefox"]:
            print("Invalid browser name. Please choose either 'chromium' or 'firefox'.")
            sys.exit(1)
    else:
        browser_name = "chromium"

    create_user(playwright, browser_name, username="docs_dude", password="docsrule!12", email="docs_dude@local.host")
