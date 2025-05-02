Feature: Sort tasks by due date
  Scenario: Sort tasks
    Given a task list with different due dates
    When sorting by Due Date
    Then the first task should be due on "2025-05-01"