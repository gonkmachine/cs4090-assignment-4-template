import streamlit as st
import subprocess
import pandas as pd
from datetime import datetime
from tasks import *

def main():
    st.title("To-Do Application")
    
    # Load existing tasks
    tasks = load_tasks()
    
    # Sidebar for adding new tasks
    st.sidebar.header("Add New Task")
    
    # Task creation form
    with st.sidebar.form("new_task_form"):
        task_title = st.text_input("Task Title")
        task_description = st.text_area("Description")
        task_priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        task_category = st.selectbox("Category", ["Work", "Personal", "School", "Other"])
        task_due_date = st.date_input("Due Date")
        allow_overdue = st.checkbox("Allow overdue task?")
        submit_button = st.form_submit_button("Add Task")

        form_valid = True

        # Validation checks
        if submit_button:
            if not task_title.strip():
                st.error("Task title is required.")
                form_valid = False

            if task_due_date < datetime.today().date() and not allow_overdue:
                st.error("Past due date not accepted.")
                form_valid = False

            if form_valid:
                new_task = {
                    "id": generate_unique_id(tasks),
                    "title": task_title,
                    "description": task_description,
                    "priority": task_priority,
                    "category": task_category,
                    "due_date": task_due_date.strftime("%Y-%m-%d"),
                    "completed": False,
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                tasks.append(new_task)
                save_tasks(tasks)
                st.sidebar.success("Task added successfully!")
    
    # Main area to display tasks
    st.header("Your Tasks")
    if "editing_task_id" not in st.session_state:
        st.session_state.editing_task_id = None

    # Filter options
    col1, col2, col3 = st.columns(3)
    with col1:
        categories = sorted(list(set([task["category"] for task in tasks])))
        filter_category = st.selectbox("Filter by Category", ["All"] + categories)
    with col2:
        filter_priority = st.selectbox("Filter by Priority", ["All", "High", "Medium", "Low"])
    with col3:
        sort_choice = st.selectbox("Sort by Field",["Default", "Due Date", "Priority"])
    
    row_checkbox = st.columns(2)
    with row_checkbox[0]:
        show_completed = st.checkbox("Show Completed Tasks")
    with row_checkbox[1]:
        delete_completed = st.button("Delete All Complete Tasks")
    
    # Apply filters
    filtered_tasks = tasks.copy()
    if filter_category != "All":
        filtered_tasks = filter_tasks_by_category(filtered_tasks, filter_category)
    if filter_priority != "All":
        filtered_tasks = filter_tasks_by_priority(filtered_tasks, filter_priority)
    filtered_tasks = sort_tasks(filtered_tasks, sort_choice)
    if not show_completed:
        filtered_tasks = [task for task in filtered_tasks if not task["completed"]]
    if delete_completed:
        incomplete_tasks = delete_complete_tasks(tasks)
        save_tasks(incomplete_tasks)
        st.rerun()

    # Display tasks
    for task in filtered_tasks:
        col1, col2 = st.columns([4, 1])
        with col1:
            if task["completed"]:
                st.markdown(f"~~**{task['title']}**~~")
            else:
                st.markdown(f"**{task['title']}**")
            st.write(task["description"])
            st.caption(f"Due: {task['due_date']} | Priority: {task['priority']} | Category: {task['category']}")
        with col2:
            if st.button("Complete" if not task["completed"] else "Undo", key=f"complete_{task['id']}"):
                for t in tasks:
                    if t["id"] == task["id"]:
                        t["completed"] = not t["completed"]
                        save_tasks(tasks)
                        st.rerun()
            if st.button("Edit", key=f"editbtn_{task['id']}"):
                st.session_state.editing_task_id = task["id"]
                st.rerun()
            if st.button("Delete", key=f"delete_{task['id']}"):
                tasks = [t for t in tasks if t["id"] != task["id"]]
                save_tasks(tasks)
                st.rerun()
        if st.session_state.editing_task_id == task["id"]:
                    new_desc = st.text_area("Edit Description", task["description"], key=f"edit_{task['id']}")
                    description_window_buttons = st.columns([4,1,1])
                    with description_window_buttons[2]:
                        if st.button("Save", key=f"save_{task['id']}"):
                            for t in tasks:
                                if t["id"] == task["id"]:
                                    t["description"] = new_desc
                                    save_tasks(tasks)
                                    st.session_state.editing_task_id = None
                                    st.rerun()
                    with description_window_buttons[1]:
                        if st.button("Cancel", key=f"cancel_{task['id']}"):
                            st.session_state.editing_task_id = None
                            st.rerun()

    # Pytest Utilities and Layout
    st.divider()
    st.header("Pytest Utilities")

    # Containers for layout and output
    button_container = st.container()
    output_container = st.container()

    # Create buttons for various test commands
    with button_container:
        row1 = st.columns(6)

        buttons = {
            "Basic Test": row1[0],
            "Coverage Test": row1[1],
            "Parameterization Test": row1[2],
            "Mock Test": row1[3],
            "BDD Test": row1[4],
            "HTML Report": row1[5]
        }

        # Get clicked button dynamically
        clicked_button = None
        for label, column in buttons.items():
            if column.button(label):
                clicked_button = label

    # Create placeholders for output and status
    output_display = output_container.empty()
    status_display = output_container.empty()

    def run_command(command):
        with st.spinner(f"Running: '{command}'..."):
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True
            )
            output_display.code(result.stdout + result.stderr, language='bash')
            if result.returncode == 0:
                status_display.success("Success")
            else:
                status_display.error("Failed")

    # Map buttons to their corresponding commands
    commands = {
        "Basic Test": "pytest -v tests/test_basic.py",
        "Coverage Test": "pytest --cov=tasks --cov-report=term-missing",
        "Parameterization Test": "pytest -v tests/test_advanced.py::test_filter_tasks_by_priority_param",
        "Mock Test": "pytest -v -k mocked tests/test_advanced.py",
        "BDD Test": "pytest -v tests/feature",
        "HTML Report": "pytest --html=report.html"
    }

    # Execute the command if a button is clicked
    if clicked_button:
        run_command(commands[clicked_button])

if __name__ == "__main__":
    main()