from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import unittest
import time

class LoginTest(unittest.TestCase):

    def setUp(self):
        # Automatically download and use the correct version of EdgeDriver
        self.browser = webdriver.Edge(EdgeChromiumDriverManager().install())
        self.browser.maximize_window()
        self.browser.implicitly_wait(10)  # Set implicit wait for elements

    def test_login(self):
        # Navigate to the login page
        self.browser.get('http://127.0.0.1:8000/login1/')
        
        # Find elements by their name or id and perform actions
        username_input = self.browser.find_element("name", "email")  # Adjust to match your form fields
        password_input = self.browser.find_element("name", "password")  # Adjust to match your form fields
        login_button = self.browser.find_element("id", "submit")  # Adjust to match your button ID or other locator
        
        # Simulate user input
        username_input.send_keys("mail2dominicpeter@gmail.com")
        password_input.send_keys("Dominic@2001")
        
        # Submit the form
        login_button.click()

        # Wait for the welcome message to appear
        time.sleep(2)  # Optional: wait for 2 seconds

        # Check for the welcome message
        welcome_text = self.browser.find_element("id", "welcome-message")  # Replace with actual ID or locator
        self.assertIn("Welcome", welcome_text.text)

        # Click on the Microsoft Edge browser image to go to the profile page
        edge_image = self.browser.find_element("id", "edge-browser-image")  # Adjust the ID to match your image's ID
        edge_image.click()

        # Wait for the profile page to load
        time.sleep(2)  # Optional: wait for the profile page to load

        # Add assertions to verify you are on the profile page
        profile_header = self.browser.find_element("id", "profile-header")  # Adjust the ID to match your profile page header
        self.assertIn("Profile", profile_header.text)

        # Click on logout
        logout_button = self.browser.find_element("id", "logout-btn")  # Adjust the ID to match your logout button's ID
        logout_button.click()

        # Optionally, wait for confirmation that the logout was successful
        time.sleep(2)  # Optional: wait for 2 seconds

    def tearDown(self):
        # Close the browser after the test
        self.browser.quit()

if __name__ == "__main__":
    unittest.main()
