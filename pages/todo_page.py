"""
Todo Page Object
Page Object for TodoMVC application (Playwright demo)

Inherits from BasePage (POO inheritance pattern)
"""
from pages.base_page import BasePage
from playwright.sync_api import Page, expect


class TodoPage(BasePage):
    """
    Todo Page Object.
    
    Represents the TodoMVC application page.
    Inherits common methods from BasePage.
    """
    
    # ============================================
    # Page Locators (Selectors)
    # ============================================
    
    # Input
    NEW_TODO_INPUT = ".new-todo"
    
    # Todo items
    TODO_ITEMS = ".todo-list li"
    TODO_ITEM_LABEL = ".todo-list li label"
    TODO_ITEM_CHECKBOX = ".todo-list li .toggle"
    TODO_ITEM_DELETE = ".todo-list li .destroy"
    
    # Filters
    FILTER_ALL = "a[href='#/']"
    FILTER_ACTIVE = "a[href='#/active']"
    FILTER_COMPLETED = "a[href='#/completed']"
    
    # Footer
    TODO_COUNT = ".todo-count"
    CLEAR_COMPLETED = ".clear-completed"
    
    
    # ============================================
    # Constructor
    # ============================================

    def __init__(self, page: Page):
        """
        Initialize TodoPage.
        
        Args:
            page: Playwright Page instance
        """
        super().__init__(page) # Call parent constructor
        self.url = "https://demo.playwright.dev/todomvc"

    # ============================================
    # Page Actions
    # ============================================

    def open(self) -> None:
        """Open Todo page"""
        self.navigate_to(self.url)

    def add_todo(self, todo_text: str) -> None:
        """
        Add a new todo item.
        
        Args:
            todo_text: Todo item text
        """
        self.fill(self.NEW_TODO_INPUT, todo_text)
        self.press_key(self.NEW_TODO_INPUT, "Enter")
        print(f"\n✔ Added todo: {todo_text}")

    def add_multiple_todos(self, todos: list) -> None:
        """
        Add multiple todo items.
        
        Args:
            todos: List of todo texts
        """
        for todo in todos:
            self.add_todo(todo)

    def complete_todo(self, todo_index: int = 0) -> None:
        """
        Complete a todo by index.
        
        Args:
            todo_index: Index of todo to complete (0-based)
        """
        checkboxes = self.page.locator(self.TODO_ITEM_CHECKBOX)
        checkboxes.nth(todo_index).check()
        print(f"\n✔ Completed todo: {todo_index}")

    def delete_todo(self, todo_index: int = 0) -> None:
        """
        Delete a todo by index.
        
        Args:
            todo_index: Index of todo to delete (0-based)
        """
        items = self.page.locator(self.TODO_ITEMS)
        item = items.nth(todo_index)

        # Hover to show delete button
        item.hover()

        # Click delete button
        delete_btn = item.locator(".destroy")
        delete_btn.click()
        print(f"\n✔ Deleted todo: {todo_index}")

    def filter_active(self) -> None:
        """Filter to show active todos only"""
        self.click(self.FILTER_ACTIVE)
        print("\n✔ Filtered active todos")

    def filter_completed(self) -> None:
        """Filter to show completed todos only"""
        self.click(self.FILTER_COMPLETED)
        print("\n✔ Filtered completed todos")

    def filter_all(self) -> None:
        """Filter to show all todos"""
        self.click(self.FILTER_ALL)
        print("\n✔ Filtered all todos")

    def clear_completed(self) -> None:
        """Clear completed todos"""
        self.click(self.CLEAR_COMPLETED)
        print("\n✔ Cleared completed todos")

    # ============================================
    # Assertions / Verifications
    # ============================================
    
    def assert_todo_exists(self, todo_text: str) -> None:
        """
        Assert todo item exists.
        
        Args:
            todo_text: Todo text to verify
        """
        # Filter for the specific item to avoid strict mode issues with the full list
        locator = self.page.locator(self.TODO_ITEM_LABEL).filter(has_text=todo_text)
        expect(locator.first).to_be_visible(timeout=self.timeout)
        print(f"\n✔ Assertion passed: Todo '{todo_text}' exists")
    
    
    def assert_todo_count(self, expected_count: int) -> None:
        """
        Assert number of visible todos.
        
        Args:
            expected_count: Expected number of todos
        """
        items = self.page.locator(self.TODO_ITEMS)
        actual_count = items.count()
        
        assert actual_count == expected_count, \
            f"Expected {expected_count} todos, got {actual_count}"
        
        print(f"\n✔ Todo count verified: {expected_count}")
    
    
    def assert_todo_completed(self, todo_index: int = 0) -> None:
        """
        Assert todo is marked as completed.
        
        Args:
            todo_index: Index of todo to check
        """
        items = self.page.locator(self.TODO_ITEMS)
        item = items.nth(todo_index)
        
        class_attr = item.get_attribute("class")
        
        assert "completed" in class_attr, \
            f"Todo at index {todo_index} is not completed"
        
        print(f"\n✔ Todo at index {todo_index} is completed")
    
    
    # ============================================
    # Get Methods
    # ============================================
    
    def get_todo_count(self) -> int:
        """
        Get number of visible todos.
        
        Returns:
            int: Number of todos
        """
        items = self.page.locator(self.TODO_ITEMS)
        count = items.count()
        print(f"\n📝 Todo count: {count}")
        return count
    
    
    def get_todo_text(self, todo_index: int = 0) -> str:
        """
        Get text of todo by index.
        
        Args:
            todo_index: Index of todo
            
        Returns:
            str: Todo text
        """
        labels = self.page.locator(self.TODO_ITEM_LABEL)
        text = labels.nth(todo_index).text_content()
        print(f"\n📝 Todo at index {todo_index}: {text}")
        return text
