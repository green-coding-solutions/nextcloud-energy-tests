import contextlib
import sys
import signal
import random
import string

from playwright.sync_api import Playwright, sync_playwright, expect

from helpers.helper_functions import log_note, get_random_text, login_nextcloud, close_modal, timeout_handler, user_sleep

DOMAIN = 'https://ncs'

def run(playwright: Playwright, browser_name: str) -> None:
    log_note(f"Launch browser {browser_name}")
    if browser_name == "firefox":
        browser = playwright.firefox.launch(headless=False)
    else:
        browser = playwright.chromium.launch(headless=False, args=['--disable-gpu', '--disable-software-rasterizer', '--ozone-platform=wayland'])
    context = browser.new_context(ignore_https_errors=True)
    page = context.new_page()

    try:
        log_note("Opening login page")
        page.goto(f"{DOMAIN}/login")

        log_note("Logging in")
        login_nextcloud(page, domain=DOMAIN)
        user_sleep()

        # Wait for the modal to load. As it seems you can't close it while it is showing the opening animation.
        log_note("Close first-time run popup")
        close_modal(page)

        log_note("Go to contacs")
        page.get_by_role("link", name="Contacts").click()
        user_sleep()

        log_note("Create new Contact")
        contact_name = "Gary McKinnon" + ''.join(random.choices(string.ascii_letters, k=5))
        page.get_by_role("button", name="New contact").click()
        page.get_by_placeholder("Name").fill(contact_name)
        page.get_by_role("button", name="Save").click()
        user_sleep()

        log_note('Validating saved contact')
        expect(page.get_by_role('heading', name=contact_name)).to_be_visible()
        expect(page.locator('div.list-item-content__name', has_text=contact_name)).to_have_count(1)
        user_sleep()

        log_note("Modify contact")
        page.get_by_role("button", name="Edit").click()
        edit_contact_name = contact_name + ''.join(random.choices(string.ascii_letters, k=5))
        page.get_by_placeholder("Name").fill(edit_contact_name)
        page.get_by_role("button", name="Save").click()
        user_sleep()

        log_note('Validating edit')
        expect(page.get_by_role('heading', name=edit_contact_name)).to_be_visible()
        expect(page.locator('div.list-item-content__name', has_text=edit_contact_name)).to_have_count(1)
        user_sleep()

        log_note("Delete the contact - Opening delete popup")
        actions_button = page.locator('button[aria-haspopup="menu"]')
        actions_button.click()

        actions_button_id = actions_button.get_attribute('id')
        menu_id = actions_button_id.replace('trigger-', '')
        menu_selector = f'ul#{menu_id}[role="menu"]'
        menu_locator = page.locator(menu_selector)
        expect(menu_locator).to_be_visible()

        log_note("Delete the contact - Clicking delete")
        delete_button = menu_locator.locator('button.action-button:has-text("Delete")')
        expect(delete_button).to_be_visible()
        delete_button.click()
        user_sleep()

        log_note('Validating delete')
        expect(page.locator('div.list-item-content__name', has_text=edit_contact_name)).to_have_count(0)
        user_sleep()

        page.close()
        log_note("Close browser")

    except Exception as e:
        if hasattr(e, 'message'): # only Playwright error class has this member
            log_note(f"Exception occurred: {e.message}")

        # set a timeout. Since the call to page.content() is blocking we need to defer it to the OS
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(20)
        #log_note(f"Page content was: {page.content()}")
        signal.alarm(0) # remove timeout signal

        raise e

    # ---------------------
    context.close()
    browser.close()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        browser_name = sys.argv[1].lower()
        if browser_name not in ["chromium", "firefox"]:
            print("Invalid browser name. Please choose either 'chromium' or 'firefox'.")
            sys.exit(1)
    else:
        browser_name = "firefox"

    with sync_playwright() as playwright:
        run(playwright, browser_name)
