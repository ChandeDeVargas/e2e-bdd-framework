"""
Multi-Browser Tests
Run same tests across different browsers

Uses pytest-playwright's native browser parameterization
"""
import pytest
from pages.todo_page import TodoPage


class TestMultiBrowser:
    """
    Tests that run on multiple browsers.
    
    Run with: pytest --browser chromium --browser firefox --browser webkit
    """
    
    def test_todo_on_browser(self, page):
        """
        Test: Add todo (runs on selected browser)
        
        Usage:
        - pytest --browser chromium
        - pytest --browser firefox
        - pytest --browser webkit
        """
        todo_page = TodoPage(page)
        todo_page.open()
        
        # Get browser name from page context
        browser_type = page.context.browser.browser_type.name
        
        todo_page.add_todo(f"Test on {browser_type}")
        todo_page.assert_todo_exists(f"Test on {browser_type}")
        
        print(f"✅ Test passed on {browser_type}")
    
    
    def test_complete_todo_on_browser(self, page):
        """
        Test: Complete todo on selected browser
        """
        todo_page = TodoPage(page)
        todo_page.open()
        
        browser_type = page.context.browser.browser_type.name
        
        todo_page.add_todo("Task to complete")
        todo_page.complete_todo(0)
        todo_page.assert_todo_completed(0)
        
        print(f"✅ Complete test passed on {browser_type}")