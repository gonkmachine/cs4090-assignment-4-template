import pytest
from datetime import datetime
from tasks import *

@pytest.fixture
def task_list():
    return [
        {"id": 1, "title": "Task 1", "priority": "High", "category": "Work", "due_date": datetime.now().strftime("%Y-%m-%d"), "completed": False, "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
        {"id": 2, "title": "Task 2", "priority": "Low", "category": "Personal", "due_date": "2004-04-15", "completed": False, "created_at": "2025-04-22 10:15:00"},
        {"id": 3, "title": "Task 3", "priority": "Medium", "category": "School", "due_date": datetime.now().strftime("%Y-%m-%d"), "completed": True, "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
    ]

# Parameterization Test: Testing filter tasks by priority with multiple priorities
@pytest.mark.parametrize("priority, expected_count", [
    ("High", 1),
    ("Low", 1),
    ("Medium", 1),
    ("Nonexistent", 0),
])

def test_filter_tasks_by_priority_param(task_list, priority, expected_count):
    filtered_tasks = filter_tasks_by_priority(task_list, priority)
    assert len(filtered_tasks) == expected_count

def test_load_tasks_with_mocked_file(task_list, mocker):
    mock_open = mocker.mock_open(read_data = json.dumps(task_list))
    mocker.patch("builtins.open", mock_open)
    result = load_tasks("test.json")
    assert result == task_list

def test_load_tasks_mocked_file_not_found(mocker):
    mocker.patch("builtins.open", side_effect = FileNotFoundError)
    result = load_tasks("null.json")
    assert result == []

def test_load_tasks_mocked_invalid_json(mocker):
    mock_file = mocker.mock_open()
    mocker.patch("builtins.open", mock_file)
    mocker.patch("json.load", side_effect=json.JSONDecodeError("Expecting value", "", 0))
    result = load_tasks("corrupt.json")
    assert result == []

def test_get_overdue_tasks_mocked_datetime(mocker):
    import tasks

    mock_now = mocker.Mock()
    mock_now.strftime.return_value = "2025-04-30"
    mock_datetime = mocker.patch("tasks.datetime")
    mock_datetime.now.return_value = mock_now

    test_tasks = [
        {"title": "Old Task", "due_date": "2025-04-01", "completed": False},
        {"title": "New Task", "due_date": "2025-05-01", "completed": False}
    ]
    overdue = get_overdue_tasks(test_tasks)
    assert len(overdue) == 1
    assert overdue[0]["title"] == "Old Task"