"""
Logging Demo
Simple test to see the logging system in action
"""
from pages.todo_page import TodoPage
from utils.logger import test_logger

class TestLoginDemo:
    """Demo logging capabilities"""
    
    def test_logging_in_action(self, page):
        """
        Test: See logging in action
        
        This test shows how the logs look
        """
        test_logger.step("Start logging test")
        
        todo_page = TodoPage(page)
        
        test_logger.step("Open todo page")
        todo_page.open()
        
        test_logger.step("Add a todo")
        todo_page.add_todo("Test con logging")
        
        test_logger.assertion("Verify that the todo exists")
        todo_page.add_todo("Test con loggingm")
        
        test_logger.info("Test completed successfully")