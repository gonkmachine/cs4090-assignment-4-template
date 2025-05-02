import pytest
from pytest_bdd import scenario, given, when, then
from tasks import save_tasks, load_tasks

@pytest.fixture
def task_file(tmp_path):
    return tmp_path / "test.json"

@scenario('../edit_task.feature', "Edit a task")
def test_edit_task():
    pass

@given('a task with description "Old description"')
def create_task_with_old_description(task_file):
    task = {
        "id": 1,
        "title": "Task",
        "description": "Old description",
        "priority": "Low",
        "category": "Work",
        "due_date": "2025-05-05",
        "completed": False,
        "created_at": ""
    }
    save_tasks([task], task_file)

@when('the user edits the description to "New description"')
def user_edits_task_description(task_file):
    tasks = load_tasks(task_file)
    tasks[0]["description"] = "New description"
    save_tasks(tasks, task_file)

@then("the task should have the updated description")
def task_should_have_updated_description(task_file):
    tasks = load_tasks(task_file)
    assert tasks[0]["description"] == "New description"