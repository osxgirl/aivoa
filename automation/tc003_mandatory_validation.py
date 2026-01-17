from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()
driver.get("http://216.48.184.249:5289/login")

# Login
driver.find_element(By.NAME, "email").send_keys("testing@aivoa.net")
driver.find_element(By.NAME, "password").send_keys("password123")
driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)

time.sleep(3)

# Navigate to Deviation form
driver.get("http://216.48.184.249:5289/quality/records/new?template_id=c5915aaf-6b3a-48b2-8b2a-190e8d1904c8")
time.sleep(3)

# Click Submit without filling fields
driver.find_element(By.XPATH, "//button[contains(text(),'Submit')]").click()
time.sleep(2)

# Verify validation message
error_message = driver.find_element(By.CLASS_NAME, "error-message")
assert error_message.is_displayed()

driver.quit()

