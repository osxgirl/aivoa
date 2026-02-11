from dotenv import load_dotenv
load_dotenv()

import time
import os

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


# --- Browser setup ---
options = Options()
options.headless = False

options.set_preference("signon.rememberSignons", False)
options.set_preference("signon.autofillForms", False)
options.set_preference("signon.management.page.breach-alerts.enabled", False)

driver = webdriver.Firefox(
    service=Service(GeckoDriverManager().install()),
    options=options
)

driver.maximize_window()
wait = WebDriverWait(driver, 15)

# --- Login ---
driver.get("http://216.48.184.249:5289/login")

email = wait.until(EC.visibility_of_element_located(
    (By.XPATH, "//input[@placeholder='name@company.com']")
))
email.send_keys(os.getenv("AIVOA_EMAIL"))

password = wait.until(EC.visibility_of_element_located(
    (By.XPATH, "//input[@type='password']")
))

password_value = os.getenv("AIVOA_PASSWORD")
if not password_value:
    raise ValueError("AIVOA_PASSWORD not loaded")

password.send_keys(password_value)

login_btn = wait.until(EC.element_to_be_clickable(
    (By.XPATH, "//button[@type='submit']")
))

#This ensures Selenium is bound to an active window
wait.until(lambda d: d.execute_script("return window.location.href") is not None)

driver.execute_script("arguments[0].click();", login_btn)

# IMPORTANT: wait for redirect after login
wait.until(EC.url_contains("/quality"))

# give React router time to fully settle
time.sleep(1)

# --- Navigate ---
driver.get(
    "http://216.48.184.249:5289/quality/records/new?template_id=c5915aaf-6b3a-48b2-8b2a-190e8d1904c8"
)

# --- Form ---
# --- Impact checkbox ---
# --- Wait for form to be fully mounted ---
wait.until(lambda d: d.execute_script("""
    return document.readyState === 'complete'
"""))

wait.until(lambda d: d.execute_script("""
    return document.querySelectorAll('input').length > 0
"""))

time.sleep(0.5)  # hydration buffer


# --- Short description ---
wait.until(lambda d: d.execute_script(
    "return document.getElementById('short_description_of_event') !== null"
))

desc = driver.execute_script(
    "return document.getElementById('short_description_of_event')"
)

driver.execute_script(
    """
    arguments[0].value = arguments[1];
    arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
    arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
    """,
    desc,
    "Temperature excursion observed during raw material storage."
)

# --- Dropdowns ---
Select(wait.until(EC.element_to_be_clickable(
    (By.ID, "preliminary_criticality")
))).select_by_visible_text("Major - Escalate to Management")

Select(wait.until(EC.element_to_be_clickable(
    (By.ID, "source_of_event")
))).select_by_visible_text("Production / Manufacturing")

Select(wait.until(EC.element_to_be_clickable(
    (By.ID, "department_owner")
))).select_by_visible_text("Production")

# --- Submit ---
submit = wait.until(EC.element_to_be_clickable(
    (By.XPATH, "//button[@type='submit']")
))
driver.execute_script("arguments[0].click();", submit)

time.sleep(3)
driver.quit()