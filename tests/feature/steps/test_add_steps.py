import pytest
from pytest_bdd import scenario, given, when, then
from tasks import save_tasks, load_tasks

@pytest.fixture
def task_file(tmp_path):
    return tmp_path / "test.json"

@scenario('../add_task.feature', "Adding step to empty task list")
def test_add_tasks():
    pass

@given("an empty task list")
def empty_task_list(task_file):
    save_tasks([], task_file)

@when("a user adds a task")
def user_adds_task(task_file):
    tasks = load_tasks(task_file)
    new_task = {
        "id": 1,
        "title": "Task 1",
        "description": "",
        "priority": "Medium",
        "category": "Work",
        "due_date": "2099-12-31",
        "completed": False,
        "created_at": "2025-04-30 10:00:00"
    }
    tasks.append(new_task)
    save_tasks(tasks, task_file)

@then("the task list should contain one task")
def task_list_should_contain_task(task_file):
    tasks = load_tasks(task_file)
    assert len(tasks) == 1