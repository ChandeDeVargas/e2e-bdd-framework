"""
Login Demo Tests
Tests for LoginDemoPage - practicing new Page Object

Uses the new BasePage improvements
"""
import pytest
from pages.login_demo_page import LoginDemoPage

pytestmark = pytest.mark.external

class TestLoginDemo:
    """
    Login demo tests.
    
    Practicing:
    - Method chaining
    - New assertions
    - Page Object Model
    """
    
    def test_login_successful_login(self, page):
        """
        Test: Successful login with valid credentials
        
        Steps:
        1. Open login page
        2. Enter valid credentials
        3. Click login
        4. Verify success
        """
        login_page = LoginDemoPage(page)
        # Method chaining in action
        login_page.open() \
            .login_with_valid_credentials()
            
        # Verify success
        login_page.assert_login_successful()
        login_page.assert_on_secure_area()
        
        # Verify logout button is enabled
        login_page.assert_logout_button_enabled()
        
        print("Test passed: Successful login.")
        
    def test_failed_login_wrong_username(self, page):
        """
        Test: Login fails with wrong username
        """
        login_page = LoginDemoPage(page)
        
        login_page.open() \
            .login("wronguser", "SuperSecretPassword!")
            
        # Verify failure
        login_page.assert_on_login_page()
        
        # Verify still on login page
        login_page.assert_on_login_page()
        
        print("Test passed: Login failed as expected")
        
        
    def test_failed_login_wrong_password(self, page):
        """
        Test: Login fails with wrong password
        """
        login_page = LoginDemoPage(page)
        
        login_page.open() \
            .login("tomsmith", "wrongpassword")
            
        login_page.assert_login_failed()
        
        # Get and print error message
        error_msg = login_page.get_flash_message()
        print(f"Error message: {error_msg}")
        
        print("Test passed: Wrong password rejected")
        
    def test_failed_login_empty_credentials(self, page):
        """
        Test: Login fails with empty fields
        """
        login_page = LoginDemoPage(page)
        login_page.open() \
            .login("", "")
            
        login_page.assert_login_failed()
        
        print("Test passed: empty credentials rejected")
        
    def test_successful_logout(self, page):
        """
        Test: Successful logout
        
        Steps:
        1. Login
        2. Logout
        3. Verify back to login page
        """
        login_page = LoginDemoPage(page)
        
        # Login first
        login_page.open() \
            .login_with_valid_credentials()
            
        login_page.assert_login_successful()
        
        # Logout
        login_page.logout()
        
        # Verify logout
        login_page.assert_logout_successful()
        login_page.assert_on_login_page()
        
        # Verify login button is visible again
        login_page.assert_login_button_visible()
        
        print("Test passed: Successful logout")
        
    def test_login_form_elements(self, page):
        """
        Test: Login form has all required elements
        
        Practicing: element count and visibility checks
        """
        login_page = LoginDemoPage(page)
        login_page.open()
        
        # Verify form visible
        login_page.assert_visible(login_page.LOGIN_FORM)
        
        # Verify inputs visible and enabled
        login_page.assert_visible(login_page.USERNAME_INPUT)
        login_page.assert_enabled(login_page.USERNAME_INPUT)
        
        login_page.assert_visible(login_page.PASSWORD_INPUT)
        login_page.assert_enabled(login_page.PASSWORD_INPUT)
        
        # Verify button visible and enabled
        login_page.assert_visible(login_page.LOGIN_BUTTON)
        login_page.assert_enabled(login_page.LOGIN_BUTTON)
        
        # Take screenshot of login form
        login_page.take_screenshot_with_timestamp("login_form")
        
        print("Test passed: All form elements present")
    
    
    @pytest.mark.parametrize("username,password", [
        ("wronguser", "SuperSecretPassword!"),
        ("tomsmith", "wrongpassword"),
        ("", ""),
        ("  ", "  "),
    ])
    def test_multiple_invalid_logins(self, page, username, password):
        """
        Test: Multiple invalid login attempts
        
        Practicing: Parametrized tests
        """
        login_page = LoginDemoPage(page)
        
        login_page.open() \
            .login(username, password)
        
        # All should fail
        login_page.assert_login_failed()
        
        print(f"Invalid login rejected: {username}/{password}")