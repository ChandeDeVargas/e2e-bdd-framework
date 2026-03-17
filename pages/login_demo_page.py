"""
Login Demo Page Object
Page to practice login on https://the-internet.herokuapp.com/login

Valid credentials:
- Username: tomsmith
- Password: SuperSecretPassword!
"""
from pages.base_page import BasePage
from playwright.sync_api import Page

class LoginDemoPage(BasePage):
    """
    Login Demo Page Object.
    
    Practice page for login/logout.
    Uses the new assertions and methods from BasePage.
    """
    
    # ============================================
    # Page URL
    # ============================================
    URL = "https://the-internet.herokuapp.com/login"
    
    # ============================================
    # Locators
    # ============================================
    
    # Inputs
    USERNAME_INPUT = "#username"
    PASSWORD_INPUT = "#password"
    
    # Buttons
    LOGIN_BUTTON = "button[type='submit']"
    LOGOUT_BUTTON = "a[href='/logout']"
    
    # Messages
    FLASH_MESSAGE = "#flash"
    SUCCESS_MESSAGE = ".flash.success"
    ERROR_MESSAGE = ".flash.error"
    
    # Page Elements
    PAGE_HEADING = "h2"
    LOGIN_FORM = "#login"
    
    # Secure area
    SECURE_AREA_HEADING = "h2"
    SECURE_AREA_TEXT = "h4.subheader"
    
    # ============================================
    # Valid Credentials (Test Data)
    # ============================================
    VALID_USERNAME = "tomsmith"
    VALID_PASSWORD = "SuperSecretPassword!"
    
    # ============================================
    # Constructor
    # ============================================
    
    def __init__(self, page: Page):
        """
        Initialize LoginDemoPage.
        
        Args:
            page: Playwright Page instance
        """
        super().__init__(page)
        
    # ============================================
    # Page Actions
    # ============================================
    
    def open(self) -> 'LoginDemoPage':
        """
        Open login page.
        
        Returns:
            LoginDemoPage: self (for method chaining)
        """
        self.navigate_to(self.URL)
        return self
    
    def enter_username(self, username: str) -> 'LoginDemoPage':
        """
        Enter username.
        
        Args:
            username: Username to enter
            
        Returns:
            LoginDemoPage: self (for method chaining)
        """
        self.fill(self.USERNAME_INPUT, username)
        return self

    def enter_password(self, password: str) -> 'LoginDemoPage':
        """
        Enter password.
        
        Args:
            password: Password to enter
            
        Returns:
            LoginDemoPage: self (for method chaining)
        """
        self.fill(self.PASSWORD_INPUT, password)
        return self
    
    def click_login(self) -> 'LoginDemoPage':
        """
        Click login button.
        
        Returns:
            LoginDemoPage: self (for method chaining)
        """
        self.click(self.LOGIN_BUTTON)
        return self
    
    def login(self, username: str, password: str) -> 'LoginDemoPage':
        """
        Perform complete login.
        
        Args:
            username: Username
            password: Password
            
        Returns:
            LoginDemoPage: self (for method chaining)
        """
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
        return self
    
    def login_with_valid_credentials(self) -> 'LoginDemoPage':
        """
        Login with default valid credentials.
        
        Returns:
            LoginDemoPage: self (for method chaining)
        """
        return self.login(self.VALID_USERNAME, self.VALID_PASSWORD)

    def logout(self) -> 'LoginDemoPage':
        """
        Logout from secure area.
        
        Returns:
            LoginDemoPage: self (for method chaining)
        """
        self.click(self.LOGOUT_BUTTON)
        return self
    
    def clear_flash_message(self) -> 'LoginDemoPage':
        """
        Close flash message.
        
        Returns:
            LoginDemoPage: self (for method chaining)
        """
        # Click X button if visible
        if self.is_visible("#flash .close"):
            self.click("#flash .close")
        return self
    
    # ============================================
    # Assertions / Verifications
    # ============================================
    
    def assert_on_login_page(self) -> None:
        """Assert user in on login page"""
        self.assert_visible(self.LOGIN_FORM)
        self.assert_text(self.PAGE_HEADING, "Login Page")
        print("On login page")
        
    def assert_login_successful(self) -> None:
        """Assert login was successful"""
        self.assert_visible(self.SUCCESS_MESSAGE)
        self.assert_text(self.SUCCESS_MESSAGE, "You logged into a secure area!")
        self.assert_visible(self.LOGOUT_BUTTON)
        print("Login successful")
    
    
    def assert_login_failed(self) -> None:
        """Assert login failed with error"""
        self.assert_visible(self.ERROR_MESSAGE)
        print("Login failed (expected)")
    
    
    def assert_on_secure_area(self) -> None:
        """Assert user is in secure area"""
        self.assert_text(self.SECURE_AREA_HEADING, "Secure Area")
        self.assert_visible(self.LOGOUT_BUTTON)
        print("In secure area")
    
    
    def assert_logout_successful(self) -> None:
        """Assert logout was successful"""
        self.assert_visible(self.SUCCESS_MESSAGE)
        self.assert_text(self.SUCCESS_MESSAGE, "You logged out of the secure area!")
        self.assert_visible(self.LOGIN_BUTTON)
        print("Logout successful")
    
    def assert_logout_button_enabled(self) -> None:
        """Assert logout button is enabled"""
        self.assert_enabled(self.LOGOUT_BUTTON)
        print("Logout button is enabled")
    
    def assert_login_button_visible(self) -> None:
        """Assert login button is visible"""
        self.assert_visible(self.LOGIN_BUTTON)
        print("Login button is visible")
    
    # ============================================
    # Get Methods
    # ============================================
    
    def get_flash_message(self) -> str:
        """
        Get flash message text.
        
        Returns:
            str: Flash message text
        """
        return self.get_text(self.FLASH_MESSAGE)
    
    
    def is_logged_in(self) -> bool:
        """
        Check if user is logged in.
        
        Returns:
            bool: True if logged in
        """
        return self.is_visible(self.LOGOUT_BUTTON)