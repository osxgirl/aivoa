# Fill required fields (example)
driver.find_element(By.NAME, "title").send_keys("Test Deviation")
driver.find_element(By.NAME, "description").send_keys("Deviation created via automation test")

# Submit form
driver.find_element(By.XPATH, "//button[contains(text(),'Submit')]").click()
time.sleep(3)

# Verify redirect or success indicator
assert "completed" in driver.current_url.lower()

