import json
import os

# --- Configuration ---
DATABASE_FILE = 'todo_database.json'

class Task:
    """Represents a single To-Do item."""
    def __init__(self, description: str, completed: bool = False):
        self.description = description
        self.completed = completed

    def __str__(self):
        """String representation of the task."""
        status = "[X]" if self.completed else "[ ]"
        return f"{status} {self.description}"

    def to_dict(self):
        """Converts the Task object to a dictionary for JSON storage."""
        return {
            "description": self.description,
            "completed": self.completed
        }

    @staticmethod
    def from_dict(data: dict):
        """Creates a Task object from a dictionary loaded from JSON."""
        return Task(
            description=data.get("description", ""),
            completed=data.get("completed", False)
        )

# --- Class + Objects / JSON Handling / File Read/Write / Exception Handling ---
class TodoList:
    """Manages the list of tasks and handles file I/O."""
    def __init__(self, filename=DATABASE_FILE):
        self.filename = filename
        self.tasks = self.load_tasks()

    def load_tasks(self) -> list[Task]:
        """Loads tasks from the JSON file. Handles file read exceptions."""
        if not os.path.exists(self.filename):
            print(f"Database file '{self.filename}' not found. Starting with an empty list.")
            return []
        
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                # Convert list of dictionaries back into a list of Task objects
                return [Task.from_dict(d) for d in data]
        except json.JSONDecodeError:
            print("Error decoding JSON from file. Starting with an empty list.")
            return []
        except IOError as e:
            print(f"File read error: {e}. Starting with an empty list.")
            return []

    def save_tasks(self):
        """Saves the current list of tasks to the JSON file. Handles file write exceptions."""
        try:
            # Convert list of Task objects to a list of dictionaries for JSON storage
            data = [task.to_dict() for task in self.tasks]
            with open(self.filename, 'w') as f:
                json.dump(data, f, indent=4)
        except IOError as e:
            print(f"Error saving to file: {e}")

    # --- Add, Edit, Delete Methods ---

    def add_task(self, description: str):
        """Adds a new task to the list."""
        new_task = Task(description)
        self.tasks.append(new_task)
        self.save_tasks()
        print(f"✅ Added task: '{description}'")

    def edit_task(self, index: int, new_description: str):
        """Edits the description of an existing task."""
        # Convert 1-based index to 0-based index
        task_index = index - 1 
        
        if 0 <= task_index < len(self.tasks):
            old_description = self.tasks[task_index].description
            self.tasks[task_index].description = new_description
            self.save_tasks()
            print(f"✏️ Task {index} updated from '{old_description}' to '{new_description}'")
        else:
            print(f"❌ Invalid task number: {index}")

    def toggle_complete(self, index: int):
        """Marks a task as complete or incomplete."""
        # Convert 1-based index to 0-based index
        task_index = index - 1 
        
        if 0 <= task_index < len(self.tasks):
            task = self.tasks[task_index]
            task.completed = not task.completed
            self.save_tasks()
            status = "completed" if task.completed else "pending"
            print(f"🔄 Task {index} marked as {status}.")
        else:
            print(f"❌ Invalid task number: {index}")

    def delete_task(self, index: int):
        """Deletes a task from the list."""
        # Convert 1-based index to 0-based index
        task_index = index - 1 
        
        if 0 <= task_index < len(self.tasks):
            deleted_task = self.tasks.pop(task_index)
            self.save_tasks()
            print(f"🗑️ Deleted task {index}: '{deleted_task.description}'")
        else:
            print(f"❌ Invalid task number: {index}")

    def view_tasks(self):
        """Prints the current list of tasks."""
        if not self.tasks:
            print("\n🎉 Your to-do list is empty! Time to add some tasks.")
            return

        print("\n--- 📋 Current To-Do List ---")
        for i, task in enumerate(self.tasks):
            print(f"{i + 1}. {task}")
        print("----------------------------\n")


# --- Main Application Logic ---
def get_valid_input(prompt, input_type=str, min_val=None, max_val=None):
    """Helper function for robust user input and exception handling."""
    while True:
        user_input = input(prompt).strip()
        if not user_input:
            print("Input cannot be empty.")
            continue
            
        if input_type == int:
            try:
                value = int(user_input)
                if (min_val is not None and value < min_val) or \
                   (max_val is not None and value > max_val):
                    print(f"Please enter a number between {min_val} and {max_val}.")
                    continue
                return value
            except ValueError:
                print("Invalid input. Please enter a valid number.")
        else:
            return user_input

def main():
    """The main function to run the To-Do List application."""
    todo_list = TodoList()
    
    print("Welcome to the To-Do List App!")

    while True:
        todo_list.view_tasks()
        
        print("\n--- Menu ---")
        print("1. **Add** a new task")
        print("2. **Edit** a task description")
        print("3. **Complete/Pending** a task")
        print("4. **Delete** a task")
        print("5. **Exit**")
        
        choice = get_valid_input("Enter your choice (1-5): ", int, 1, 5)

        if choice == 1:
            description = get_valid_input("Enter the new task description: ")
            todo_list.add_task(description)
            
        elif choice == 2:
            if todo_list.tasks:
                index = get_valid_input("Enter the number of the task to edit: ", int, 1, len(todo_list.tasks))
                new_description = get_valid_input("Enter the new description: ")
                todo_list.edit_task(index, new_description)
            else:
                print("No tasks to edit.")

        elif choice == 3:
            if todo_list.tasks:
                index = get_valid_input("Enter the number of the task to toggle status: ", int, 1, len(todo_list.tasks))
                todo_list.toggle_complete(index)
            else:
                print("No tasks to mark as complete.")

        elif choice == 4:
            if todo_list.tasks:
                index = get_valid_input("Enter the number of the task to delete: ", int, 1, len(todo_list.tasks))
                todo_list.delete_task(index)
            else:
                print("No tasks to delete.")

        elif choice == 5:
            print("Exiting application. Have a productive day!")
            break

if __name__ == "__main__":
    main()