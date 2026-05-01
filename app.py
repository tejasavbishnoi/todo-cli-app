import json
from pathlib import Path


TASKS_FILE = Path("tasks.json")


def load_tasks():
    """Load tasks from the JSON file, creating an empty list when needed."""
    if not TASKS_FILE.exists():
        save_tasks([])
        return []

    try:
        with TASKS_FILE.open("r", encoding="utf-8") as file:
            tasks = json.load(file)
    except json.JSONDecodeError:
        print("Warning: tasks.json is invalid. Starting with an empty task list.")
        return []

    if not isinstance(tasks, list):
        print("Warning: tasks.json has the wrong format. Starting with an empty task list.")
        return []

    return tasks


def save_tasks(tasks):
    """Write all tasks back to disk using readable JSON formatting."""
    with TASKS_FILE.open("w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4)


def get_next_id(tasks):
    """Return the next available integer ID."""
    if not tasks:
        return 1
    return max(task.get("id", 0) for task in tasks) + 1


def add_task(tasks):
    """Ask the user for a task title and add it to the list."""
    title = input("Enter task title: ").strip()

    if not title:
        print("Task title cannot be empty.")
        return

    task = {
        "id": get_next_id(tasks),
        "title": title,
        "completed": False,
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task added: {title}")


def view_tasks(tasks):
    """Print every task in a clear, compact table."""
    if not tasks:
        print("No tasks found.")
        return

    print("\nTasks:")
    print("-" * 50)
    print(f"{'ID':<5} {'Status':<12} Title")
    print("-" * 50)

    for task in tasks:
        status = "Done" if task.get("completed") else "Pending"
        print(f"{task.get('id', ''):<5} {status:<12} {task.get('title', '')}")

    print("-" * 50)


def find_task_by_id(tasks, task_id):
    """Find a task by ID, or return None when it does not exist."""
    for task in tasks:
        if task.get("id") == task_id:
            return task
    return None


def read_task_id(prompt):
    """Read and validate a numeric task ID from user input."""
    raw_id = input(prompt).strip()

    try:
        task_id = int(raw_id)
    except ValueError:
        print("Please enter a valid numeric ID.")
        return None

    if task_id <= 0:
        print("Task ID must be a positive number.")
        return None

    return task_id


def complete_task(tasks):
    """Mark an existing task as completed."""
    if not tasks:
        print("No tasks found.")
        return

    task_id = read_task_id("Enter task ID to complete: ")
    if task_id is None:
        return

    task = find_task_by_id(tasks, task_id)
    if task is None:
        print(f"No task found with ID {task_id}.")
        return

    if task.get("completed"):
        print("Task is already completed.")
        return

    task["completed"] = True
    save_tasks(tasks)
    print(f"Task completed: {task.get('title', '')}")


def delete_task(tasks):
    """Delete an existing task from the list."""
    if not tasks:
        print("No tasks found.")
        return

    task_id = read_task_id("Enter task ID to delete: ")
    if task_id is None:
        return

    task = find_task_by_id(tasks, task_id)
    if task is None:
        print(f"No task found with ID {task_id}.")
        return

    tasks.remove(task)
    save_tasks(tasks)
    print(f"Task deleted: {task.get('title', '')}")


def show_menu():
    """Display the main menu."""
    print("\nTo-Do List")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Complete Task")
    print("4. Delete Task")
    print("5. Exit")


def main():
    """Run the menu loop until the user chooses to exit."""
    tasks = load_tasks()

    while True:
        show_menu()
        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            view_tasks(tasks)
        elif choice == "3":
            complete_task(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()
