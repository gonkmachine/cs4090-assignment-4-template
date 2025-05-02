import pytest
from pytest_bdd import scenario, given, when, then
from tasks import sort_tasks, save_tasks, load_tasks

@pytest.fixture
def task_file(tmp_path):
    return tmp_path / "test.json"

@pytest.fixture
def shared():
    return {}

@scenario('../sort_tasks.feature', "Sort tasks")
def test_sort_tasks():
    pass

@given("a task list with different due dates")
def create_tasks(task_file):
    tasks = [
        {"id": 1, "title": "Task A", "priority": "High", "category": "", "due_date": "2025-05-10", "completed": False, "description": "", "created_at": ""},
        {"id": 2, "title": "Task B", "priority": "High", "category": "", "due_date": "2025-05-01", "completed": False, "description": "", "created_at": ""}
    ]
    save_tasks(tasks, task_file)

@when('sorting by Due Date')
def sort_by_due_date(task_file, shared):
    tasks = load_tasks(task_file)
    shared["sorted"] = sort_tasks(tasks, "Due Date")

@then('the first task should be due on "2025-05-01"')
def check_sorted_order(shared):
    assert shared["sorted"][0]["due_date"] == "2025-05-01"