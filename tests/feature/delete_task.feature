Feature: Delete all completed tasks
Scenario: Delete all completed tasks
  Given a list of tasks with some completed
  When all completed tasks are deleted
  Then only incomplete tasks should remain