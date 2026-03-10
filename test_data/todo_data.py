"""
Test Data Classes
POO approach to managing test data

Provides clean, reusable test data with validation
"""
from dataclasses import dataclass
from typing import List
from datetime import datetime


@dataclass
class TodoItem:
    """
    Todo item data class.
    
    Represents a single todo item with validation.
    
    Attributes:
        text: Todo text
        completed: Completion status
        created_at: Creation timestamp
    """
    text: str
    completed: bool = False
    created_at: datetime = None
    
    def __post_init__(self):
        """Validate and set defaults after initialization"""
        if not self.text or not self.text.strip():
            raise ValueError("Todo text cannot be empty")
        
        if self.created_at is None:
            self.created_at = datetime.now()
        
        # Trim whitespace
        self.text = self.text.strip()
    
    
    def mark_completed(self) -> None:
        """Mark todo as completed"""
        self.completed = True
    
    
    def mark_active(self) -> None:
        """Mark todo as active (not completed)"""
        self.completed = False
    
    
    def __str__(self) -> str:
        """String representation"""
        status = "✓" if self.completed else "○"
        return f"{status} {self.text}"


class TodoTestData:
    """
    Test data provider for todo tests.
    
    Centralized test data management (POO pattern).
    """
    
    # ============================================
    # Sample Todo Items
    # ============================================
    
    SAMPLE_TODOS = [
        "Buy groceries",
        "Learn Playwright",
        "Learn pytest-bdd",
        "Build awesome framework",
        "Write documentation"
    ]
    
    PRIORITY_TODOS = [
        "🔴 High priority task",
        "🟡 Medium priority task",
        "🟢 Low priority task"
    ]
    
    WORK_TODOS = [
        "Review pull requests",
        "Write unit tests",
        "Update documentation",
        "Fix bug #123"
    ]
    
    PERSONAL_TODOS = [
        "Call dentist",
        "Buy birthday gift",
        "Plan vacation",
        "Pay bills"
    ]
    
    
    # ============================================
    # Factory Methods (POO Pattern)
    # ============================================
    
    @staticmethod
    def create_todo(text: str, completed: bool = False) -> TodoItem:
        """
        Create a TodoItem instance.
        
        Args:
            text: Todo text
            completed: Initial completion status
            
        Returns:
            TodoItem: New todo item
        """
        return TodoItem(text=text, completed=completed)
    
    
    @staticmethod
    def create_sample_todos(count: int = 5) -> List[TodoItem]:
        """
        Create sample todo items.
        
        Args:
            count: Number of todos to create
            
        Returns:
            List[TodoItem]: List of todo items
        """
        return [
            TodoItem(text=todo) 
            for todo in TodoTestData.SAMPLE_TODOS[:count]
        ]
    
    
    @staticmethod
    def create_priority_todos() -> List[TodoItem]:
        """
        Create priority todo items.
        
        Returns:
            List[TodoItem]: Priority todos
        """
        return [
            TodoItem(text=todo) 
            for todo in TodoTestData.PRIORITY_TODOS
        ]
    
    
    @staticmethod
    def create_mixed_todos(active_count: int = 3, 
                          completed_count: int = 2) -> List[TodoItem]:
        """
        Create mix of active and completed todos.
        
        Args:
            active_count: Number of active todos
            completed_count: Number of completed todos
            
        Returns:
            List[TodoItem]: Mixed todos
        """
        todos = []
        
        # Active todos
        for i in range(active_count):
            todos.append(TodoItem(
                text=TodoTestData.SAMPLE_TODOS[i],
                completed=False
            ))
        
        # Completed todos
        for i in range(completed_count):
            todos.append(TodoItem(
                text=TodoTestData.SAMPLE_TODOS[active_count + i],
                completed=True
            ))
        
        return todos
    
    
    # ============================================
    # Validation Methods
    # ============================================
    
    @staticmethod
    def validate_todo_text(text: str) -> bool:
        """
        Validate todo text.
        
        Args:
            text: Todo text to validate
            
        Returns:
            bool: True if valid
        """
        if not text or not text.strip():
            return False
        
        if len(text) > 500:  # Max length
            return False
        
        return True
    
    
    @staticmethod
    def get_invalid_todos() -> List[str]:
        """
        Get list of invalid todo texts for negative testing.
        
        Returns:
            List[str]: Invalid todo texts
        """
        return [
            "",           # Empty
            "   ",        # Only whitespace
            "a" * 501,    # Too long
        ]