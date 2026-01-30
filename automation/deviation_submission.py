from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time
import os
password.send_keys(os.getenv("AIVOA_PASSWORD"))

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
email.send_keys(os.getenv("AIVOA_EMAIL", "testing@aivoa.net"))

password = wait.until(EC.visibility_of_element_located(
    (By.XPATH, "//input[@type='password']")
))
password.send_keys(os.getenv("AIVOA_PASSWORD", "dummy_password"))

login_btn = wait.until(EC.element_to_be_clickable(
    (By.XPATH, "//button[@type='submit']")
))
driver.execute_script("arguments[0].click();", login_btn)

# --- Navigate ---
driver.get(
    "http://216.48.184.249:5289/quality/records/new?template_id=c5915aaf-6b3a-48b2-8b2a-190e8d1904c8"
)

# --- Form ---
desc = wait.until(EC.presence_of_element_located(
    (By.NAME, "short_description_of_event")
))
desc.send_keys(
    "Temperature excursion observed during raw material storage. No adverse product impact identified."
)

criticality = Select(wait.until(
    EC.element_to_be_clickable((By.ID, "preliminary_criticality"))
))
criticality.select_by_visible_text("Major - Escalate to Management")

wait.until(lambda d: len(
    Select(d.find_element(By.ID, "source_of_event")).options
) > 1)

Select(driver.find_element(By.ID, "source_of_event")) \
    .select_by_visible_text("Production / Manufacturing")

Select(driver.find_element(By.ID, "department_owner")) \
    .select_by_visible_text("Production")

# Intentionally skipping product impact checkbox
# Default unchecked state is correct for this scenario

submit = wait.until(EC.element_to_be_clickable(
    (By.XPATH, "//button[contains(text(),'Submit')]")
))
driver.execute_script("arguments[0].click();", submit)

time.sleep(3)
driver.quit()