Feature: Edit task description
  Scenario: Edit a task
    Given a task with description "Old description"
    When the user edits the description to "New description"
    Then the task should have the updated description