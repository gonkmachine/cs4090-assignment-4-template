Feature: Add a task
  Scenario: Adding step to empty task list
    Given an empty task list
    When a user adds a task
    Then the task list should contain one task