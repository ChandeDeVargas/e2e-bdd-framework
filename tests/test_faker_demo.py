"""
Faker Demo Tests
Shows how to use Faker to generate test data
"""
from pages.todo_page import TodoPage
from utils.logger import test_logger


class TestFakerDemo:
    """Demo of Faker capabilities"""
    
    def test_todos_with_random_data(self, page, faker):
        """
        Test: Add todos with random data from Faker
        
        Each time you run this test, it will have different data
        """
        test_logger.step("Generate random todos with Faker")
        
        todo_page = TodoPage(page)
        todo_page.open()
        
        # Generate 5 random todos
        random_todos = faker.random_todos(count=5)
        
        test_logger.info(f"Generated todos: {random_todos}")
        
        # Add each one
        for todo_text in random_todos:
            test_logger.step(f"Add todo: {todo_text}")
            todo_page.add_todo(todo_text)
        
        # Verify count
        todo_page.assert_todo_count(5)
        
        test_logger.info("Random todos with data added correctly")
    
    
    def test_faker_user_data(self, faker):
        """
        Test: Generate user data with Faker
        
        This test only shows the data, doesn't use Playwright
        """
        test_logger.step("Generate random user data")
        
        # Generate a user
        user = faker.create_user()
        
        test_logger.info("Generated user:")
        test_logger.info(f"  Username: {user['username']}")
        test_logger.info(f"  Email: {user['email']}")
        test_logger.info(f"  Full Name: {user['full_name']}")
        test_logger.info(f"  Phone: {user['phone']}")
        test_logger.info(f"  Password: {user['password']}")
        
        # Verify it has all fields
        assert "username" in user
        assert "email" in user
        assert "@" in user["email"]  # Validate email format
        
        test_logger.info("User data generated correctly")
    
    
    def test_multiple_users(self, faker):
        """Test: Generate multiple users"""
        test_logger.step("Generate 10 random users")
        
        users = faker.create_users(count=10)
        
        # Verify all have unique email
        emails = [user["email"] for user in users]
        assert len(emails) == len(set(emails)), "Emails should be unique"
        
        test_logger.info(f"{len(users)} unique users generated")
        
        # Show first 3
        for i, user in enumerate(users[:3], 1):
            test_logger.info(f"{i}. {user['full_name']} ({user['email']})")