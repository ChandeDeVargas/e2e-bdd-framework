Feature: Todo Management
    As a user
    I want to manage my todo items
    So that I can keep track of tasks

    Background:
        Given I am on the todo page

    @smoke @critical
    Scenario: Add a single todo item
        When I add a todo "Buy groceries"
        Then I should see the todo "Buy groceries"
        And the todo count should be 1

    @smoke
    Scenario: Add multiple todo items
    When I add the following todos:
      | todo                    |
      | Learn Playwright        |
      | Learn pytest-bdd        |
      | Build awesome framework |
    Then the todo count should be 3
    And I should see the todo "Learn Playwright"
    And I should see the todo "Learn pytest-bdd"

    @regression
    Scenario: Complete a todo item
        When I add a todo "Task to complete"
        And I complete the todo "Task to complete"
        Then the todo "Task to complete" should be marked as completed

    @regression
    Scenario: Delete a todo item
        When I add a todo "Task to delete"
        And I add a todo "Task to keep"
        Then the todo count should be 2
        When I delete the todo "Task to delete"
        Then the todo count should be 1
        And I should not see the todo "Task to delete"

    @regression
    Scenario: Filter active todos
        When I add a todo "Active task"
        And I add a todo "Task to complete"
        And i complete the todo "Task to complete"
        When I filter by "Active"
        Then the todo count should be 1
        And I should see the todo "Active task"

    @regression
    Scenario: Filter completed todos
        When I add a todo "Task 1"
        And I add a todo "Task 2"
        And I complete the todo "Task 1"
        When I filter by "Completed"
        Then the todo count should be 1
        And I should see the todo "Task 1"

    @regression
    Scenario: Clear completed todos
        When I add a todo "Task 1"
        And I add a todo "Task 2"
        And I complete the todo "Task 1"
        When I clear completed todos
        Then the todo count should be 1
        And I should see the todo "Task 2"

    @smoke
    Scenario Outline: Add todos with different priorities
        When I add a todo "<todo_text>"
        Then I should see the todo "<todo_text>"
        And the todo count should be 1

    Examples:
      | todo_text           |
      | High priority task  |
      | Medium priority     |
      | Low priority item   |