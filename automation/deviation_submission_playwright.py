from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os

load_dotenv()

EMAIL = os.getenv("AIVOA_EMAIL")
PASSWORD = os.getenv("AIVOA_PASSWORD")

DEVIATION_DATA = {
    "short_description": "Temperature excursion observed during raw material storage.",
    "criticality": "Major - Processing Hold",
    "event_category": "Manufacturing / Process",
    "source": "Production / Manufacturing"
}


def login(page):
    page.goto("http://216.48.184.249:5289/login")
    page.get_by_placeholder("name@company.com").fill(EMAIL)
    page.locator("input[type='password']").fill(PASSWORD)
    page.get_by_role("button", name="Sign in").click()
    page.wait_for_url("**/quality**")


def navigate_to_deviation(page):
    page.goto("http://216.48.184.249:5289/quality/log-event")
    page.get_by_text("Deviation").click()
    page.get_by_role("button", name="Continue").click()
    page.wait_for_selector("#short_description_of_event")


def fill_deviation_form(page, data):
    page.locator("#short_description_of_event").fill(data["short_description"])
    page.locator("#preliminary_criticality").select_option(label=data["criticality"])
    page.locator("#event_category").select_option(value=data["event_category"])
    page.locator("#source_of_event").select_option(value=data["source"])


def disable_ai_overlay(page):
    page.evaluate("""
    () => {
        const aiInput = document.querySelector('textarea[placeholder="Ask AIVOA AI"]');
        if (aiInput) {
            const panel = aiInput.closest('div.fixed');
            if (panel) {
                panel.style.pointerEvents = 'none';
            }
        }
    }
    """)


def submit_form(page):
    page.get_by_role("button", name="Submit").click(force=True)


def run():
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        login(page)
        navigate_to_deviation(page)
        fill_deviation_form(page, DEVIATION_DATA)
        disable_ai_overlay(page)
        submit_form(page)

        page.wait_for_timeout(3000)
        browser.close()


if __name__ == "__main__":
    run()
