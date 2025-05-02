import pytest
import json
from datetime import datetime
from tasks import *

@pytest.fixture
def tasks():
    return [
        {"id": 1, "title": "Task 1", "priority": "High", "category": "Work", "due_date": datetime.now().strftime("%Y-%m-%d"), "completed": False, "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
        {"id": 2, "title": "Task 2", "priority": "Low", "category": "Personal", "due_date": "2004-04-15", "completed": False, "created_at": "2025-04-22 10:15:00"},
        {"id": 3, "title": "Task 3", "priority": "Medium", "category": "School", "due_date": datetime.now().strftime("%Y-%m-%d"), "completed": True, "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
    ]

def test_load_tasks(tmp_path, tasks):
    TEST_TASKS_FILE = tmp_path / "test.json"
    NULL_TASKS_FILE = tmp_path / "null.json"
    INVALID_TASKS_FILE = tmp_path / "invalid.json"

    #Valid JSON
    TEST_TASKS_FILE.write_text(json.dumps(tasks))

    #Invalid JSON
    INVALID_TASKS_FILE.write_text("{ JsonDecodeError test }")

    # Case 1: Valid JSON
    test_tasks = load_tasks(TEST_TASKS_FILE)
    assert len(test_tasks) == 3

    # Case 2: FileNotFound
    test_tasks = load_tasks(NULL_TASKS_FILE)
    assert test_tasks == []

    # Case 3: Invalid/Corrupt JSON
    test_tasks = load_tasks(INVALID_TASKS_FILE)
    assert test_tasks == []

def test_save_tasks(tmp_path, tasks):
    TEST_TASKS_FILE = tmp_path / "test.json"

    save_tasks(tasks, TEST_TASKS_FILE)
    with open(TEST_TASKS_FILE, "r") as f:
        loaded_data = json.load(f)
    
    assert loaded_data == tasks

def test_generate_unique_id(tasks):
    empty_tasks = []

    # Case 1: Tasks list is empty
    empty_id = generate_unique_id(empty_tasks)
    assert empty_id == 1

    # Case 2: Tasks list is populated
    new_id = generate_unique_id(tasks)
    assert new_id == 4

def test_filter_tasks_by_priority(tasks):
    high_priority_tasks = filter_tasks_by_priority(tasks, "High")
    assert len(high_priority_tasks) == 1
    assert high_priority_tasks[0]["priority"] == "High"

def test_filter_tasks_by_category(tasks):
    work_tasks = filter_tasks_by_category(tasks, "Work")
    assert len(work_tasks) == 1
    assert work_tasks[0]["category"] == "Work"

def test_filter_tasks_by_completion(tasks):
    completed_tasks = filter_tasks_by_completion(tasks, completed=True)
    incomplete_tasks = filter_tasks_by_completion(tasks, completed=False)
    
    assert len(completed_tasks) == 1
    assert completed_tasks[0]["title"] == "Task 3"
    assert len(incomplete_tasks) == 2

def test_search_tasks(tasks):
    found_tasks = search_tasks(tasks, "Task 1")
    assert len(found_tasks) == 1
    assert found_tasks[0]["title"] == "Task 1"

def test_get_overdue_tasks(tasks):
    overdue_tasks = get_overdue_tasks(tasks)
    assert len(overdue_tasks) == 1
    assert overdue_tasks[0]["title"] == "Task 2"
