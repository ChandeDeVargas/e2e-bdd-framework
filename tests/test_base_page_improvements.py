"""
Test Base Page Improvements
Quick tests to verify new methods work
"""
from pages.todo_page import TodoPage


class TestBasePageImprovements:
    """Test new BasePage methods"""
    
    def test_new_assertions(self, page):
        """Test: New assertion methods work"""
        todo_page = TodoPage(page)
        todo_page.open()
        
        # Add some todos first
        todo_page.add_todo("Test 1")
        todo_page.add_todo("Test 2")
        todo_page.add_todo("Test 3")
        
        # Test assert_element_count
        todo_page.assert_element_count(".todo-list li", 3)
        
        # Test assert_url_contains (existing)
        todo_page.assert_url_contains("todomvc")
        
        # Test assert_visible (existing)
        todo_page.assert_visible(".new-todo")
        
        # Test assert_enabled
        todo_page.assert_enabled(".new-todo")
        
        print("All new assertions working!")
    
    
    def test_scroll_methods(self, page):
        """Test: Scroll methods work"""
        todo_page = TodoPage(page)
        todo_page.open()
        
        # Add many todos to enable scroll
        for i in range(20):
            todo_page.add_todo(f"Todo {i+1}")
        
        # Test scroll methods
        todo_page.scroll_to_bottom()
        todo_page.wait_for_timeout(500)
        
        todo_page.scroll_to_top()
        todo_page.wait_for_timeout(500)
        
        todo_page.scroll_by_pixels(0, 300)
        
        print("Scroll methods working!")
    
    
    def test_screenshot_with_timestamp(self, page):
        """Test: Screenshot with timestamp works"""
        todo_page = TodoPage(page)
        todo_page.open()
        
        todo_page.add_todo("Screenshot test")
        
        # Take screenshot with timestamp
        filepath = todo_page.take_screenshot_with_timestamp("test_screenshot")
        
        # Verify file was created
        import os
        assert os.path.exists(filepath)
        
        print(f"Screenshot created: {filepath}")
    
    
    def test_hover_method(self, page):
        """Test: Hover method works"""
        todo_page = TodoPage(page)
        todo_page.open()
        
        todo_page.add_todo("Hover test")
        
        # Hover over todo item
        todo_page.hover(".todo-list li")
        todo_page.wait_for_timeout(500)
        
        print("Hover method working!")