import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def login(driver, base_url, logger):
    driver.get(base_url + "/login")
    try:
        user_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "username")))
        pass_input = driver.find_element(By.ID, "password")
        login_btn = driver.find_element(By.ID, "login-btn")
        user_input.send_keys("testuser")
        pass_input.send_keys("testpassword")
        login_btn.click()
        WebDriverWait(driver, 10).until(EC.url_contains("/dashboard"))
    except Exception as e:
        logger.error("Login error: " + str(e))
        pytest.fail("Login failed")

def test_add_post_after_login(driver, base_url, logger):
    login(driver, base_url, logger)
    try:
        create_post_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "create-post-btn")))
        create_post_btn.click()
        time.sleep(1)
        title_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "post-title")))
        description_input = driver.find_element(By.ID, "post-description")
        content_input = driver.find_element(By.ID, "post-content")
        submit_btn = driver.find_element(By.ID, "submit-post-btn")
        post_title = "UI Test Post"
        title_input.send_keys(post_title)
        description_input.send_keys("UI Test Description")
        content_input.send_keys("UI Test Content")
        time.sleep(1)
        submit_btn.click()
        time.sleep(2)
        post_titles = driver.find_elements(By.CLASS_NAME, "post-title")
        titles = [elem.text for elem in post_titles]
        assert post_title in titles, "Post title not found on page after creation"
    except Exception as e:
        logger.error("Add post error: " + str(e))
        pytest.fail("Add post test failed")

def test_contact_us_form(driver, base_url, logger):
    login(driver, base_url, logger)
    try:
        contact_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "contact-us-btn")))
        contact_btn.click()
        time.sleep(1)
        name_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "contact-name")))
        email_input = driver.find_element(By.ID, "contact-email")
        message_input = driver.find_element(By.ID, "contact-message")
        submit_contact = driver.find_element(By.ID, "contact-submit-btn")
        name_input.send_keys("Test Name")
        email_input.send_keys("test@example.com")
        message_input.send_keys("Test message")
        time.sleep(1)
        submit_contact.click()
        alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
        alert_text = alert.text
        alert.accept()
        assert alert_text != "", "Alert text is empty"
    except Exception as e:
        logger.error("Contact Us form error: " + str(e))
        pytest.fail("Contact Us form test failed")
