import json
import os
from datetime import datetime

TASK_FILE = "tasks.json"

# ANSI Colors
COLORS = {
    "high": "\033[91m",    # Red
    "medium": "\033[93m",  # Yellow
    "low": "\033[92m",     # Green
    "reset": "\033[0m"
}

# Load tasks from file
def load_tasks():
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, 'r') as f:
            return json.load(f)
    return []

# Save tasks to file
def save_tasks():
    with open(TASK_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)

# Show menu
def show_menu():
    print("\n=== ENHANCED TO-DO LIST ===")
    print("1. View All Tasks")
    print("2. Add Task")
    print("3. Complete Task")
    print("4. Delete Task")
    print("5. Search Tasks")
    print("6. Sort Tasks")
    print("7. Exit")

# View tasks
def view_tasks():
    if not tasks:
        print("No tasks yet.")
        return
    print("\nYour Tasks:")
    for i, task in enumerate(tasks, start=1):
        color = COLORS.get(task['priority'].lower(), "")
        reset = COLORS['reset']
        status = "✔️" if task["completed"] else "❌"
        print(f"{i}. {color}{task['title']} [{task['priority'].capitalize()} | Due: {task['due_date']}]{reset} [{status}]")

# Add task
def add_task():
    title = input("Enter task title: ")
    due_date = input("Enter due date (YYYY-MM-DD): ")
    priority = input("Enter priority (High/Medium/Low): ").lower()
    task = {
        "title": title,
        "due_date": due_date,
        "priority": priority,
        "completed": False
    }
    tasks.append(task)
    save_tasks()
    print("Task added.")

# Complete task
def complete_task():
    view_tasks()
    try:
        index = int(input("Enter task number to complete: ")) - 1
        if 0 <= index < len(tasks):
            tasks[index]["completed"] = True
            save_tasks()
            print("Task marked as completed.")
        else:
            print("Invalid number.")
    except ValueError:
        print("Please enter a valid number.")

# Delete task
def delete_task():
    view_tasks()
    try:
        index = int(input("Enter task number to delete: ")) - 1
        if 0 <= index < len(tasks):
            removed = tasks.pop(index)
            save_tasks()
            print(f"Deleted: {removed['title']}")
        else:
            print("Invalid number.")
    except ValueError:
        print("Please enter a valid number.")

# Search tasks
def search_tasks():
    keyword = input("Enter keyword to search: ").lower()
    found = [task for task in tasks if keyword in task['title'].lower()]
    if found:
        print("\nSearch Results:")
        for i, task in enumerate(found, start=1):
            color = COLORS.get(task['priority'].lower(), "")
            reset = COLORS['reset']
            status = "✔️" if task["completed"] else "❌"
            print(f"{i}. {color}{task['title']} [{task['priority'].capitalize()} | Due: {task['due_date']}]{reset} [{status}]")
    else:
        print("No matching tasks found.")

# Sort tasks
def sort_tasks():
    print("\nSort by:")
    print("1. Due Date")
    print("2. Priority")
    choice = input("Choose an option: ")
    if choice == '1':
        tasks.sort(key=lambda x: datetime.strptime(x['due_date'], "%Y-%m-%d"))
        print("Sorted by due date.")
    elif choice == '2':
        priority_order = {'high': 1, 'medium': 2, 'low': 3}
        tasks.sort(key=lambda x: priority_order.get(x['priority'], 4))
        print("Sorted by priority.")
    else:
        print("Invalid choice.")
    save_tasks()

# Main loop
if __name__ == "__main__":
    tasks = load_tasks()
    while True:
        show_menu()
        option = input("Choose an option (1-7): ")
        if option == '1':
            view_tasks()
        elif option == '2':
            add_task()
        elif option == '3':
            complete_task()
        elif option == '4':
            delete_task()
        elif option == '5':
            search_tasks()
        elif option == '6':
            sort_tasks()
        elif option == '7':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")
