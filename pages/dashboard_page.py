"""
Dashboard Page Object
Demonstrates advanced POO patterns

Features:
- Class methods (@classmethod)
- Static methods (@staticmethod)
- Context manager (__enter__, __exit__)
- Type hints
"""
from pages.base_page import BasePage
from playwright.sync_api import Page
from typing import List, Dict, Optional
from datetime import datetime


class DashboardPage(BasePage):
    """
    Dashboard Page Object with advanced POO.
    
    Demonstrates:
    - @classmethod
    - @staticmethod
    - Context manager protocol
    - Advanced type hints
    """
    
    # ============================================
    # Locators
    # ============================================
    
    WELCOME_MESSAGE = ".post-title"
    LOGOUT_BUTTON = "a[href*='logout']"
    
    
    # ============================================
    # Constructor
    # ============================================
    
    def __init__(self, page: Page):
        """Initialize DashboardPage"""
        super().__init__(page)
        self._session_start = None
    
    
    # ============================================
    # Context Manager Protocol (POO Advanced)
    # ============================================
    
    def __enter__(self) -> 'DashboardPage':
        """
        Enter context manager.
        
        Called when entering 'with' block.
        
        Returns:
            DashboardPage: self
        """
        self._session_start = datetime.now()
        print(f"📊 Dashboard session started: {self._session_start}")
        return self
    
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        """
        Exit context manager.
        
        Called when exiting 'with' block.
        
        Args:
            exc_type: Exception type (if any)
            exc_val: Exception value (if any)
            exc_tb: Exception traceback (if any)
            
        Returns:
            bool: False to propagate exceptions
        """
        session_end = datetime.now()
        duration = (session_end - self._session_start).total_seconds()
        
        print(f"📊 Dashboard session ended")
        print(f"📊 Session duration: {duration:.2f} seconds")
        
        # Take screenshot if there was an error
        if exc_type is not None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.take_screenshot(f"screenshots/dashboard_error_{timestamp}.png")
            print(f"📸 Error screenshot taken")
        
        return False  # Don't suppress exceptions
    
    
    # ============================================
    # Class Methods (@classmethod)
    # ============================================
    
    @classmethod
    def from_login(cls, page: Page, username: str, password: str) -> 'DashboardPage':
        """
        Create DashboardPage by logging in first.
        
        Factory method using @classmethod.
        
        Args:
            page: Playwright page
            username: Login username
            password: Login password
            
        Returns:
            DashboardPage: Dashboard instance
        """
        from pages.login_page import LoginPage
        
        login_page = LoginPage(page)
        login_page.open()
        login_page.login(username, password)
        
        # Return dashboard instance
        dashboard = cls(page)
        print(f"✅ Dashboard created via login: {username}")
        return dashboard
    
    
    # ============================================
    # Static Methods (@staticmethod)
    # ============================================
    
    @staticmethod
    def format_session_duration(seconds: float) -> str:
        """
        Format session duration.
        
        Static method - doesn't need instance or class.
        
        Args:
            seconds: Duration in seconds
            
        Returns:
            str: Formatted duration
        """
        if seconds < 60:
            return f"{seconds:.1f} seconds"
        else:
            minutes = seconds / 60
            return f"{minutes:.1f} minutes"
    
    
    @staticmethod
    def validate_username(username: str) -> bool:
        """
        Validate username format.
        
        Args:
            username: Username to validate
            
        Returns:
            bool: True if valid
        """
        if not username or len(username) < 3:
            return False
        
        if not username.replace("_", "").replace("-", "").isalnum():
            return False
        
        return True
    
    
    # ============================================
    # Public Methods
    # ============================================
    
    def logout(self) -> None:
        """Logout from dashboard"""
        self.click(self.LOGOUT_BUTTON)
        print("✅ Logged out from dashboard")
    
    
    def assert_welcome_message_visible(self) -> None:
        """Assert welcome message is visible"""
        self.assert_visible(self.WELCOME_MESSAGE)
        print("✅ Welcome message visible")
    
    
    def get_welcome_text(self) -> str:
        """
        Get welcome message text.
        
        Returns:
            str: Welcome text
        """
        return self.get_text(self.WELCOME_MESSAGE)