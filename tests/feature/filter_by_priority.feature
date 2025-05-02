Feature: Filter tasks by priority
Scenario: Filter tasks by high
  Given a task list with priorities "Low", "Medium", and "High"
  When filtering by "High"
  Then only 1 task should be returned