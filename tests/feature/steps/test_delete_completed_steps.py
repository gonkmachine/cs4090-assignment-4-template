import pytest
from pytest_bdd import scenario, given, when, then
from tasks import save_tasks, load_tasks, delete_complete_tasks

@pytest.fixture
def task_file(tmp_path):
    return tmp_path / "test.json"

@scenario('../delete_task.feature', "Delete all completed tasks")
def test_delete_tasks():
    pass

@given("a list of tasks with some completed")
def setup_tasks_with_some_completed(task_file):
    tasks = [
        {"id": 1, "completed": True, "title": "Done", "priority": "", "category": "", "due_date": "", "description": "", "created_at": ""},
        {"id": 2, "completed": False, "title": "Not Done", "priority": "", "category": "", "due_date": "", "description": "", "created_at": ""}
    ]
    save_tasks(tasks, task_file)

@when("all completed tasks are deleted")
def delete_completed_tasks(task_file):
    tasks = load_tasks(task_file)
    incomplete_tasks = delete_complete_tasks(tasks)
    save_tasks(incomplete_tasks, task_file)

@then("only incomplete tasks should remain")
def assert_only_incomplete_tasks(task_file):
    tasks = load_tasks(task_file)
    assert all(not t["completed"] for t in tasks)