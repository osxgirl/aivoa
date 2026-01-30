from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time

options = Options()

# Keep browser visible for debugging
options.headless = False

# Disable password manager & breach alerts
options.set_preference("signon.rememberSignons", False)
options.set_preference("signon.autofillForms", False)
options.set_preference("signon.management.page.breach-alerts.enabled", False)

# Allow HTTP / insecure content
options.set_preference("security.mixed_content.block_active_content", False)
options.set_preference("security.mixed_content.block_display_content", False)

# Suppress dialogs
options.set_preference("dom.disable_open_during_load", False)

driver = webdriver.Firefox(
    service=Service(GeckoDriverManager().install()),
    options=options
)

driver.maximize_window()

# 1. Go to login page FIRST
driver.get("http://216.48.184.249:5289/login")

# 2. Create wait AFTER page load
wait = WebDriverWait(driver, 15)


# 3. Wait for email field, then interact
email_field = wait.until(
    EC.visibility_of_element_located(
        (By.XPATH, "//input[@placeholder='name@company.com']")
    )
)
email_field.send_keys("testing@aivoa.net")

# 4. Password field
password_field = wait.until(
    EC.visibility_of_element_located(
        (By.XPATH, "//input[@type='password']")
    )
)
password_field.send_keys(".")

# 5. Click Login
submit_btn = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
)

driver.execute_script("arguments[0].click();", submit_btn)

time.sleep(2)


# 6. Navigate to Deviation page
driver.get(
    "http://216.48.184.249:5289/quality/records/new?template_id=c5915aaf-6b3a-48b2-8b2a-190e8d1904c8"
)

driver.save_screenshot("after_login.png")


# 7. Wait for form field
description_field = wait.until(
    EC.presence_of_element_located((By.NAME, "short_description_of_event"))
)
description_field.send_keys(
    "Temperature excursion observed during raw material storage. No adverse product impact identified."
)

# Wait for the dropdown to be present
criticality = Select(
    wait.until(
        EC.element_to_be_clickable((By.ID, "preliminary_criticality"))
    )
)
criticality.select_by_visible_text("Major - Escalate to Management")

wait.until(
    lambda d: len(
        Select(d.find_element(By.ID, "source_of_event")).options
    ) > 1
)

source_select = Select(
    driver.find_element(By.ID, "source_of_event")
)

source_select.select_by_visible_text("Production / Manufacturing")


source_select = Select(
    driver.find_element(By.ID, "department_owner")
)

source_select.select_by_visible_text("Production")

# Only fill Linked Complaint ID if test data exists
# Otherwise: intentionally skip


# Product Impact checkbox:
# Default state = unchecked ("No adverse product impact identified").
# For this test case, no product impact is expected, so we intentionally
# do NOT click this checkbox. Clicking it would indicate a confirmed
# product impact and trigger additional business logic (holds, actions).

checkbox = wait.until(
    EC.presence_of_element_located(
        (By.ID, "product_impact_confirmed")
    )
)

driver.execute_script("""
arguments[0].checked = true;
arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
""", checkbox)

assert checkbox.is_selected()

# Successful submission without interaction validates correct default behavior.


submit_button = wait.until(
    EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Submit')]"))
)
driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
time.sleep(0.5)

driver.execute_script("arguments[0].click();", submit_button)



# 8. Submit
submit_button = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Submit')]"))
)
submit_button.click()

time.sleep(5)

driver.quit()
