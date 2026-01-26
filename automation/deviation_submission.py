from selenium import webdriver
from selenium.webdriver.common.by import By
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
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
password_field.send_keys("1234567notthepaswordhaha")

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
    EC.presence_of_element_located((By.NAME, "description"))
)
description_field.send_keys(
    "Temperature excursion observed during raw material storage. No adverse product impact identified."
)

# 8. Submit
submit_button = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Submit')]"))
)
submit_button.click()

time.sleep(5)

driver.quit()
