"""
Advanced Login Tests
Demonstrates POO patterns with LoginPage

Features:
- Method chaining (fluent interface)
- Properties
- Multi-browser
"""
import pytest
from pages.login_page import LoginPage


class TestLoginAdvanced:
    """
    Advanced login tests demonstrating POO patterns.
    """
    
    def test_login_with_method_chaining(self, page):
        """
        Test: Login using method chaining (fluent interface)
        
        Demonstrates fluent interface pattern
        """
        login_page = LoginPage(page)
        
        # Method chaining in action
        login_page.open() \
            .enter_username("student") \
            .enter_password("Password123") \
            .click_submit()
        
        # Verify
        login_page.assert_login_successful()
        
        print("✅ Method chaining test passed")
    
    
    def test_login_with_valid_credentials(self, page):
        """
        Test: Login with predefined valid credentials
        
        Uses class constant for test data
        """
        login_page = LoginPage(page)
        
        login_page.open()
        login_page.login_with_valid_credentials()
        
        # Verify using property
        assert login_page.is_logged_in, "User should be logged in"
        
        login_page.assert_login_successful()
        
        print(f"✅ Logged in as: {login_page.current_username}")
    
    
    def test_login_with_invalid_credentials(self, page):
        """
        Test: Login with invalid credentials
        
        Verifies error handling
        """
        login_page = LoginPage(page)
        
        login_page.open()
        login_page.login("invalid_user", "wrong_password")
        
        # Verify login failed
        assert not login_page.is_logged_in, "User should NOT be logged in"
        
        # Verify error message using property
        assert login_page.error_message_visible, "Error message should be visible"
        
        login_page.assert_login_failed()
        
        print("✅ Invalid login handled correctly")
    
    
    @pytest.mark.parametrize("credentials", LoginPage.INVALID_CREDENTIALS)
    def test_multiple_invalid_logins(self, page, credentials):
        """
        Test: Multiple invalid login attempts
        
        Demonstrates parametrization with class data
        """
        login_page = LoginPage(page)
        
        login_page.open()
        login_page.login(
            credentials["username"],
            credentials["password"]
        )
        
        # All should fail
        assert not login_page.is_logged_in
        
        print(f"✅ Invalid login blocked: {credentials['username']}")
    
    
    def test_empty_username_validation(self, page):
        """
        Test: Empty username validation
        
        Tests private validation method
        """
        login_page = LoginPage(page)
        login_page.open()
        
        # Should raise ValueError (caught by private method)
        with pytest.raises(ValueError, match="Username cannot be empty"):
            login_page.enter_username("")
        
        print("✅ Validation working correctly")


class TestDashboardAdvanced:
    """
    Advanced dashboard tests demonstrating POO.
    """
    
    def test_dashboard_context_manager(self, page):
        """
        Test: Dashboard with context manager
        
        Demonstrates __enter__ and __exit__
        """
        from pages.dashboard_page import DashboardPage
        
        # Create via factory method (@classmethod)
        dashboard = DashboardPage.from_login(
            page,
            "student",
            "Password123"
        )
        
        # Use as context manager
        with dashboard as dash:
            dash.assert_welcome_message_visible()
            welcome = dash.get_welcome_text()
            print(f"Welcome message: {welcome}")
        
        # Session stats printed automatically on exit
        print("✅ Context manager test passed")
    
    
    def test_static_methods(self):
        """
        Test: Static methods
        
        Demonstrates @staticmethod usage
        """
        from pages.dashboard_page import DashboardPage
        
        # Test format_session_duration
        formatted = DashboardPage.format_session_duration(65.5)
        assert "minute" in formatted
        
        formatted_short = DashboardPage.format_session_duration(30.0)
        assert "second" in formatted_short
        
        # Test validate_username
        assert DashboardPage.validate_username("student")
        assert DashboardPage.validate_username("user_123")
        assert not DashboardPage.validate_username("ab")  # Too short
        assert not DashboardPage.validate_username("")     # Empty
        
        print("✅ Static methods working correctly")