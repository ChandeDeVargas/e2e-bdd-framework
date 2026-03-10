"""
Login Page Object
Demonstrates advanced POO patterns

Features:
- Property decorators
- Private methods
- Validation
- Fluent interface (method chaining)
"""
from pages.base_page import BasePage
from playwright.sync_api import Page
from typing import Optional


class LoginPage(BasePage):
    """
    Login Page Object with advanced POO patterns.
    
    Demonstrates:
    - @property decorators
    - Private methods (__)
    - Method chaining (fluent interface)
    - Validation logic
    """
    
    # ============================================
    # Page URL
    # ============================================
    
    URL = "https://practicetestautomation.com/practice-test-login/"
    
    
    # ============================================
    # Locators (Class Constants)
    # ============================================
    
    # Input fields
    USERNAME_INPUT = "#username"
    PASSWORD_INPUT = "#password"
    
    # Buttons
    SUBMIT_BUTTON = "#submit"
    
    # Messages
    SUCCESS_MESSAGE = ".post-title"
    ERROR_MESSAGE = "#error"
    
    # Logout
    LOGOUT_BUTTON = "a[href*='logout']"
    
    
    # ============================================
    # Valid Credentials (Test Data)
    # ============================================
    
    VALID_USERNAME = "student"
    VALID_PASSWORD = "Password123"
    
    INVALID_CREDENTIALS = [
        {"username": "invalid", "password": "invalid"},
        {"username": "student", "password": "wrongpass"}
    ]
    
    
    # ============================================
    # Constructor
    # ============================================
    
    def __init__(self, page: Page):
        """
        Initialize LoginPage.
        
        Args:
            page: Playwright Page instance
        """
        super().__init__(page)
        self._is_logged_in = False
    
    
    # ============================================
    # Properties (POO - @property decorator)
    # ============================================
    
    @property
    def is_logged_in(self) -> bool:
        """
        Check if user is logged in.
        
        Returns:
            bool: True if logged in
        """
        return self._is_logged_in
    
    
    @property
    def current_username(self) -> Optional[str]:
        """
        Get current logged-in username.
        
        Returns:
            str: Username if logged in, None otherwise
        """
        if self._is_logged_in:
            return self._current_user
        return None
    
    
    @property
    def error_message_visible(self) -> bool:
        """
        Check if error message is visible.
        
        Returns:
            bool: True if error visible
        """
        return self.is_visible(self.ERROR_MESSAGE)
    
    
    # ============================================
    # Public Methods (Fluent Interface)
    # ============================================
    
    def open(self) -> 'LoginPage':
        """
        Open login page.
        
        Returns:
            LoginPage: self (for method chaining)
        """
        self.navigate_to(self.URL)
        return self
    
    
    def enter_username(self, username: str) -> 'LoginPage':
        """
        Enter username.
        
        Args:
            username: Username to enter
            
        Returns:
            LoginPage: self (for method chaining)
        """
        self.__validate_input(username, "Username")
        self.fill(self.USERNAME_INPUT, username)
        return self
    
    
    def enter_password(self, password: str) -> 'LoginPage':
        """
        Enter password.
        
        Args:
            password: Password to enter
            
        Returns:
            LoginPage: self (for method chaining)
        """
        self.__validate_input(password, "Password")
        self.fill(self.PASSWORD_INPUT, password)
        return self
    
    
    def click_submit(self) -> 'LoginPage':
        """
        Click submit button.
        
        Returns:
            LoginPage: self (for method chaining)
        """
        self.click(self.SUBMIT_BUTTON)
        return self
    
    
    def login(self, username: str, password: str) -> 'LoginPage':
        """
        Perform complete login action.
        
        Args:
            username: Username
            password: Password
            
        Returns:
            LoginPage: self (for method chaining)
        """
        self.enter_username(username)
        self.enter_password(password)
        self.click_submit()
        
        # Check if login successful
        if self.__is_login_successful():
            self._is_logged_in = True
            self._current_user = username
            print(f"✅ Login successful: {username}")
        else:
            self._is_logged_in = False
            print(f"❌ Login failed: {username}")
        
        return self
    
    
    def login_with_valid_credentials(self) -> 'LoginPage':
        """
        Login with default valid credentials.
        
        Returns:
            LoginPage: self (for method chaining)
        """
        return self.login(self.VALID_USERNAME, self.VALID_PASSWORD)
    
    
    def logout(self) -> 'LoginPage':
        """
        Logout from application.
        
        Returns:
            LoginPage: self (for method chaining)
        """
        if self._is_logged_in:
            self.click(self.LOGOUT_BUTTON)
            self._is_logged_in = False
            self._current_user = None
            print("✅ Logged out successfully")
        
        return self
    
    
    # ============================================
    # Assertion Methods
    # ============================================
    
    def assert_login_successful(self) -> None:
        """Assert login was successful"""
        self.assert_visible(self.SUCCESS_MESSAGE)
        self.assert_text(self.SUCCESS_MESSAGE, "Logged In Successfully")
        print("✅ Assertion: Login successful")
    
    
    def assert_login_failed(self) -> None:
        """Assert login failed with error"""
        self.assert_visible(self.ERROR_MESSAGE)
        print("✅ Assertion: Login failed (expected)")
    
    
    def assert_error_message_contains(self, expected_text: str) -> None:
        """
        Assert error message contains text.
        
        Args:
            expected_text: Expected error text
        """
        self.assert_text(self.ERROR_MESSAGE, expected_text)
        print(f"✅ Assertion: Error contains '{expected_text}'")
    
    
    # ============================================
    # Private Methods (POO - __ prefix)
    # ============================================
    
    def __validate_input(self, value: str, field_name: str) -> None:
        """
        Validate input value (private method).
        
        Args:
            value: Input value
            field_name: Field name for error message
            
        Raises:
            ValueError: If validation fails
        """
        if not value or not value.strip():
            raise ValueError(f"{field_name} cannot be empty")
    
    
    def __is_login_successful(self) -> bool:
        """
        Check if login was successful (private method).
        
        Returns:
            bool: True if successful
        """
        try:
            self.wait_for_selector(self.SUCCESS_MESSAGE, state="visible")
            return True
        except:
            return False
    
    
    # ============================================
    # Get Methods
    # ============================================
    
    def get_error_message(self) -> str:
        """
        Get error message text.
        
        Returns:
            str: Error message
        """
        return self.get_text(self.ERROR_MESSAGE)