"""
Intermediate Features Demo
Combines logging + Faker in a real test
"""
from pages.todo_page import TodoPage
from utils.logger import test_logger


class TestIntermediateFeatures:
    """Demo: Logging + Faker together"""
    
    def test_complete_workflow_with_logging_and_faker(self, page, faker):
        """
        Test: Complete workflow with all improvements
        
        Demonstrates:
        - Professional logging
        - Random data with Faker
        - Enhanced assertions
        - Screenshots with timestamp
        """
        test_logger.test_start("Complete Workflow Test")
        
        # ============================================
        # Setup
        # ============================================
        test_logger.step("Initialize todo page")
        todo_page = TodoPage(page)
        todo_page.open()
        
        # ============================================
        # Generate data with Faker
        # ============================================
        test_logger.step("Generate random todos with Faker")
        random_todos = faker.random_todos(count=3)
        
        test_logger.info("Todos to add:")
        for i, todo in enumerate(random_todos, 1):
            test_logger.info(f"  {i}. {todo}")
        
        # ============================================
        # Add todos
        # ============================================
        test_logger.step("Add todos to application")
        for todo_text in random_todos:
            todo_page.add_todo(todo_text)
        
        # ============================================
        # Verifications
        # ============================================
        test_logger.step("Verify todos added")
        todo_page.assert_todo_count(3)
        test_logger.assertion("Count correct: 3 todos")
        
        # Verify each one exists
        for todo_text in random_todos:
            todo_page.assert_todo_exists(todo_text)
            test_logger.assertion(f"Todo exists: {todo_text}")
        
        # ============================================
        # Complete first todo
        # ============================================
        test_logger.step("Complete first todo")
        todo_page.complete_todo(0)
        todo_page.assert_todo_completed(0)
        test_logger.assertion("First todo completed")
        
        # ============================================
        # Final screenshot
        # ============================================
        test_logger.step("Take final screenshot")
        screenshot_path = todo_page.take_screenshot_with_timestamp("workflow_complete")
        test_logger.info(f"Screenshot saved: {screenshot_path}")
        
        # ============================================
        # Test successful
        # ============================================
        test_logger.info("Complete workflow executed successfully")
        test_logger.test_end("Complete Workflow Test", "PASSED")