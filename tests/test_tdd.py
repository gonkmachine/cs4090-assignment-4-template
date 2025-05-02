import pytest
from datetime import datetime
from tasks import sort_tasks, edit_task, delete_complete_tasks

@pytest.fixture
def tasks():
    return [
        {"id": 1, "title": "Task 1", "priority": "High", "category": "Work", "due_date": "2025-04-30", "completed": False, "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
        {"id": 2, "title": "Task 2", "priority": "Low", "category": "Personal", "due_date": "2004-04-15", "completed": True, "created_at": "2025-04-22 10:15:00"},
        {"id": 3, "title": "Task 3", "priority": "Medium", "category": "School", "due_date": "2025-04-30", "completed": True, "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
    ]

def test_edit_tasks(tasks):
    updated_tasks = edit_task(tasks, 1, "This is a new description")
    assert updated_tasks[0]["description"] == "This is a new description"

def test_sort_tasks_by_due_date(tasks):
    sorted_tasks = sort_tasks(tasks, "Priority")
    assert [t["id"] for t in sorted_tasks] == [1, 3, 2]

def test_sort_tasks_by_priority(tasks):
    sorted_tasks = sort_tasks(tasks, "Due Date")
    assert [t["id"] for t in sorted_tasks] == [2, 1, 3]

def test_delete_complete_tasks(tasks):
    incomplete_tasks = delete_complete_tasks(tasks)
    assert len(incomplete_tasks) == 1
    assert all(not t["completed"] for t in incomplete_tasks)
    assert [t["id"] for t in incomplete_tasks] == [1]
