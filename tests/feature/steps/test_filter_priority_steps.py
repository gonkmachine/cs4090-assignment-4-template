import pytest
from pytest_bdd import scenario, given, when, then
from tasks import filter_tasks_by_priority, save_tasks, load_tasks

@pytest.fixture
def task_file(tmp_path):
    return tmp_path / "test.json"

@pytest.fixture
def shared():
    return {}

@scenario('../filter_by_priority.feature', "Filter tasks by high")
def test_filter_by_high_priority():
    pass

@given('a task list with priorities "Low", "Medium", and "High"')
def create_task_list(task_file):
    tasks = [
        {"id": 1, "title": "Low P", "priority": "Low", "category": "", "due_date": "2025-05-10", "completed": False, "description": "", "created_at": ""},
        {"id": 2, "title": "High P", "priority": "High", "category": "", "due_date": "2025-05-10", "completed": False, "description": "", "created_at": ""},
        {"id": 3, "title": "Medium P", "priority": "Medium", "category": "", "due_date": "2025-05-10", "completed": False, "description": "", "created_at": ""}
    ]
    save_tasks(tasks, task_file)

@when('filtering by "High"')
def filter_high_priority(task_file, shared):
    tasks = load_tasks(task_file)
    shared["filtered"] = filter_tasks_by_priority(tasks, "High")

@then("only 1 task should be returned")
def check_filtered_tasks(shared):
    assert len(shared["filtered"]) == 1