"""
Todo Step Definitions
BDD step implementations for todo feature

Connects Gherkin steps to Page Objects (POO pattern)
"""
from pytest_bdd import given, when, then, scenarios, parsers
from pages.todo_page import TodoPage


# ============================================
# Load Scenarios from Feature File
# ============================================

# This loads all scenarios from the feature file
scenarios('todo_management.feature')


# ============================================
# Given Steps (Setup/Preconditions)
# ============================================

@given('I am on the todo page')
def open_todo_page(page):
    """
    Open the todo page.
    
    Args:
        page: Playwright page fixture
    """
    todo_page = TodoPage(page)
    todo_page.open()
    
    # Store page object in page for reuse
    page.todo_page = todo_page
    
    print("✅ Step: I am on the todo page")


# ============================================
# When Steps (Actions)
# ============================================

@when(parsers.parse('I add a todo "{todo_text}"'))
def add_todo(page, todo_text):
    """
    Add a single todo.
    
    Args:
        page: Playwright page with todo_page attached
        todo_text: Todo text to add
    """
    page.todo_page.add_todo(todo_text)
    print(f"✅ Step: I add a todo '{todo_text}'")


@when('I add the following todos:')
def add_multiple_todos(page, datatable):
    """
    Add multiple todos from data table.
    
    Args:
        page: Playwright page with todo_page attached
        datatable: pytest-bdd datatable fixture
    """
    # datatable is a list of lists, excluding the header 'todo'
    todos = [row[0] for row in datatable[1:]]
    page.todo_page.add_multiple_todos(todos)
    print(f"✅ Step: I add {len(todos)} todos")


@when(parsers.parse('I complete the todo "{todo_text}"'))
def complete_todo(page, todo_text):
    """
    Complete a specific todo by text.
    
    Args:
        page: Playwright page
        todo_text: Todo text to complete
    """
    # Find todo index by text
    todo_index = find_todo_index_by_text(page, todo_text)
    page.todo_page.complete_todo(todo_index)
    print(f"✅ Step: I complete the todo '{todo_text}'")


@when(parsers.parse('I delete the todo "{todo_text}"'))
def delete_todo(page, todo_text):
    """
    Delete a specific todo by text.
    
    Args:
        page: Playwright page
        todo_text: Todo text to delete
    """
    todo_index = find_todo_index_by_text(page, todo_text)
    page.todo_page.delete_todo(todo_index)
    print(f"✅ Step: I delete the todo '{todo_text}'")


@when(parsers.parse('I filter by "{filter_type}"'))
def filter_todos(page, filter_type):
    """
    Filter todos by type.
    
    Args:
        page: Playwright page
        filter_type: Filter type (Active, Completed, All)
    """
    filter_map = {
        'Active': page.todo_page.filter_active,
        'Completed': page.todo_page.filter_completed,
        'All': page.todo_page.filter_all
    }
    
    filter_func = filter_map.get(filter_type)
    if filter_func:
        filter_func()
        print(f"✅ Step: I filter by '{filter_type}'")
    else:
        raise ValueError(f"Unknown filter type: {filter_type}")


@when('I clear completed todos')
def clear_completed(page):
    """
    Clear all completed todos.
    
    Args:
        page: Playwright page
    """
    page.todo_page.clear_completed()
    print("✅ Step: I clear completed todos")


# ============================================
# Then Steps (Assertions/Verifications)
# ============================================

@then(parsers.parse('I should see the todo "{todo_text}"'))
def verify_todo_exists(page, todo_text):
    """
    Verify todo exists in the list.
    
    Args:
        page: Playwright page
        todo_text: Todo text to verify
    """
    page.todo_page.assert_todo_exists(todo_text)
    print(f"✅ Step: I should see the todo '{todo_text}'")


@then(parsers.parse('I should not see the todo "{todo_text}"'))
def verify_todo_not_exists(page, todo_text):
    """
    Verify todo does NOT exist in the list.
    
    Args:
        page: Playwright page
        todo_text: Todo text that should not exist
    """
    # Check if todo text is visible
    locator = page.locator(f"text={todo_text}")
    
    try:
        assert locator.count() == 0, \
            f"Todo '{todo_text}' should not be visible"
        print(f"✅ Step: I should not see the todo '{todo_text}'")
    except AssertionError:
        print(f"❌ Todo '{todo_text}' is still visible")
        raise


@then(parsers.parse('the todo count should be {count:d}'))
def verify_todo_count(page, count):
    """
    Verify number of visible todos.
    
    Args:
        page: Playwright page
        count: Expected todo count
    """
    page.todo_page.assert_todo_count(count)
    print(f"✅ Step: the todo count should be {count}")


@then(parsers.parse('the todo "{todo_text}" should be marked as completed'))
def verify_todo_completed(page, todo_text):
    """
    Verify todo is marked as completed.
    
    Args:
        page: Playwright page
        todo_text: Todo text to check
    """
    todo_index = find_todo_index_by_text(page, todo_text)
    page.todo_page.assert_todo_completed(todo_index)
    print(f"✅ Step: the todo '{todo_text}' should be marked as completed")


# ============================================
# Helper Functions
# ============================================

def find_todo_index_by_text(page, todo_text: str) -> int:
    """
    Find todo index by text content.
    
    Args:
        page: Playwright page
        todo_text: Todo text to find
        
    Returns:
        int: Index of todo (0-based)
        
    Raises:
        ValueError: If todo not found
    """
    labels = page.locator(".todo-list li label")
    count = labels.count()
    
    for i in range(count):
        text = labels.nth(i).text_content()
        if text == todo_text:
            return i
    
    raise ValueError(f"Todo '{todo_text}' not found")