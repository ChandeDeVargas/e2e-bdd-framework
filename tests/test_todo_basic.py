"""
Basic Todo Tests
Simple tests to verify setup and Page Object Model

These are traditional pytest tests (not BDD yet)
"""
import pytest
from pages.todo_page import TodoPage

class TestTodoBasic:
    """
    Basic Todo functionality tests.
    
    Tests the Page Object Model and Playwright setup.
    """
    def test_add_single_todo(self, page):
        """
        Test: Add a single todo item
        
        Verifies:
        - Todo can be added
        - Todo appears in list
        - Count is correct
        """
        # Initialize page object
        todo_page = TodoPage(page)

        # Open page
        todo_page.open()

        # Add todo
        todo_page.add_todo("Buy PC Gamer")

        # Verify
        todo_page.assert_todo_exists("Buy PC Gamer")
        todo_page.assert_todo_count(1)

        print("\n✔ Test: Add a single todo item passed")

    def test_add_multiple_todos(self, page):
        """
        Test: Add multiple todo items
        
        Verifies:
        - Multiple todos can be added
        - All todos appear in list
        - Count is correct
        """
        todo_page = TodoPage(page)
        todo_page.open()

        # Add multiple todos
        todos = ["Learn Playwright", "Learn pytest-bdd", "Build a project"]
        todo_page.add_multiple_todos(todos)

        # Verify
        todo_page.assert_todo_count(3)

        print("\n✔ Test: Add multiple todos passed")

    def test_complete_todo(self, page):
        """
        Test: Complete a todo item
        
        Verifies:
        - Todo can be marked as completed
        - Completed status is visible
        """
        todo_page = TodoPage(page)
        todo_page.open()
        
        # Add and complete
        todo_page.add_todo("Task to complete")
        todo_page.complete_todo(0)
        
        # Verify
        todo_page.assert_todo_completed(0)
        
        print("\n✔ Test passed: Todo completed")
    
    
    def test_delete_todo(self, page):
        """
        Test: Delete a todo item
        
        Verifies:
        - Todo can be deleted
        - Count updates correctly
        """
        todo_page = TodoPage(page)
        todo_page.open()
        
        # Add todos
        todo_page.add_todo("Task to delete")
        todo_page.add_todo("Task to keep")
        
        # Verify initial count
        todo_page.assert_todo_count(2)
        
        # Delete first todo
        todo_page.delete_todo(0)
        
        # Verify new count
        todo_page.assert_todo_count(1)
        
        print("\n✔ Test passed: Todo deleted")