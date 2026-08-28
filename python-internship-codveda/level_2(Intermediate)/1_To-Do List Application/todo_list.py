"""
To-Do List Application - Python Development Internship
Codveda Technologies
Author: Suresh Das
Date: August 2026
"""

import json
import os
import time
from datetime import datetime
from typing import List, Dict, Optional


class Task:
    """Represents a single task in the to-do list."""
    
    def __init__(self, task_id: int, description: str, completed: bool = False):
        self.id = task_id
        self.description = description
        self.completed = completed
        self.created_at = datetime.now().isoformat()
        self.completed_at = None
    
    def to_dict(self) -> Dict:
        """Convert task to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "description": self.description,
            "completed": self.completed,
            "created_at": self.created_at,
            "completed_at": self.completed_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Task':
        """Create a Task object from dictionary data."""
        task = cls(data["id"], data["description"], data["completed"])
        task.created_at = data.get("created_at", datetime.now().isoformat())
        task.completed_at = data.get("completed_at")
        return task
    
    def mark_done(self):
        """Mark the task as completed."""
        if not self.completed:
            self.completed = True
            self.completed_at = datetime.now().isoformat()
    
    def __str__(self) -> str:
        """String representation of the task."""
        status = "✅" if self.completed else "⭕"
        done_mark = f" (Done: {self.completed_at[:10]})" if self.completed_at else ""
        return f"{status} [{self.id}] {self.description}{done_mark}"


class ToDoList:
    """Main to-do list application class."""
    
    def __init__(self, filename: str = "tasks.json"):
        self.filename = filename
        self.tasks: List[Task] = []
        self.next_id = 1
        self.load_tasks()
    
    def load_tasks(self):
        """Load tasks from JSON file."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as file:
                    data = json.load(file)
                    self.tasks = [Task.from_dict(task_data) for task_data in data]
                    # Update next_id based on existing tasks
                    if self.tasks:
                        self.next_id = max(task.id for task in self.tasks) + 1
                    print(f"📂 Loaded {len(self.tasks)} tasks from {self.filename}")
            except json.JSONDecodeError:
                print(f"⚠️ Warning: {self.filename} is corrupted. Starting with empty list.")
                self.tasks = []
            except Exception as e:
                print(f"❌ Error loading tasks: {e}")
                self.tasks = []
        else:
            print(f"📂 No existing task file found. Starting fresh.")
    
    def save_tasks(self):
        """Save tasks to JSON file."""
        try:
            data = [task.to_dict() for task in self.tasks]
            with open(self.filename, 'w') as file:
                json.dump(data, file, indent=2)
            print(f"💾 Tasks saved successfully to {self.filename}")
        except Exception as e:
            print(f"❌ Error saving tasks: {e}")
    
    def add_task(self, description: str) -> Task:
        """Add a new task to the list."""
        if not description or not description.strip():
            raise ValueError("Task description cannot be empty.")
        
        task = Task(self.next_id, description.strip())
        self.tasks.append(task)
        self.next_id += 1
        self.save_tasks()
        return task
    
    def delete_task(self, task_id: int) -> bool:
        """Delete a task by its ID."""
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                del self.tasks[i]
                self.save_tasks()
                return True
        return False
    
    def mark_done(self, task_id: int) -> bool:
        """Mark a task as completed by its ID."""
        for task in self.tasks:
            if task.id == task_id:
                if task.completed:
                    print(f"⚠️ Task {task_id} is already marked as done.")
                    return True
                task.mark_done()
                self.save_tasks()
                return True
        return False
    
    def get_tasks(self, show_completed: bool = True) -> List[Task]:
        """Get all tasks, optionally filtering completed ones."""
        if show_completed:
            return self.tasks
        return [task for task in self.tasks if not task.completed]
    
    def list_tasks(self, show_completed: bool = True):
        """Display all tasks in a formatted manner."""
        tasks = self.get_tasks(show_completed)
        
        if not tasks:
            print("\n📋 No tasks found.")
            return
        
        print("\n" + "=" * 60)
        print("📋 YOUR TO-DO LIST")
        print("=" * 60)
        
        pending = [t for t in tasks if not t.completed]
        completed = [t for t in tasks if t.completed]
        
        if pending:
            print(f"\n📌 PENDING TASKS ({len(pending)}):")
            print("-" * 40)
            for task in pending:
                print(f"   {task}")
        
        if show_completed and completed:
            print(f"\n✅ COMPLETED TASKS ({len(completed)}):")
            print("-" * 40)
            for task in completed:
                print(f"   {task}")
        
        print("\n" + "=" * 60)
        print(f"📊 Summary: {len(pending)} pending, {len(completed)} completed")
        print("=" * 60)
    
    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Find a task by its ID."""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None


def display_menu():
    """Display the main menu."""
    print("\n" + "=" * 50)
    print("      📝 TO-DO LIST APPLICATION")
    print("=" * 50)
    print("\nMenu:")
    print("  1. 📋 View all tasks")
    print("  2. ➕ Add a new task")
    print("  3. ✅ Mark task as done")
    print("  4. 🗑️  Delete a task")
    print("  5. 📊 View pending tasks only")
    print("  6. 🧹 Clear all tasks")
    print("  7. 💾 Save and exit")
    print("-" * 50)


def get_integer_input(prompt: str, min_val: int = 1) -> int:
    """Get a valid integer input from the user."""
    while True:
        try:
            value = int(input(prompt))
            if value >= min_val:
                return value
            print(f"❌ Please enter a number greater than or equal to {min_val}.")
        except ValueError:
            print("❌ Invalid input! Please enter a number.")


def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    """Main application loop."""
    todo = ToDoList()
    
    print("\n🚀 Welcome to the To-Do List Application!")
    print(f"📅 {datetime.now().strftime('%A, %B %d, %Y')}")
    print("-" * 50)
    
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == '1':
            todo.list_tasks(show_completed=True)
        
        elif choice == '2':
            description = input("\n📝 Enter task description: ").strip()
            if description:
                try:
                    task = todo.add_task(description)
                    print(f"✅ Task added successfully! (ID: {task.id})")
                except ValueError as e:
                    print(f"❌ {e}")
            else:
                print("❌ Task description cannot be empty.")
        
        elif choice == '3':
            task_id = get_integer_input("🔢 Enter task ID to mark as done: ")
            if todo.mark_done(task_id):
                print(f"✅ Task {task_id} marked as completed!")
            else:
                print(f"❌ Task with ID {task_id} not found.")
        
        elif choice == '4':
            task_id = get_integer_input("🔢 Enter task ID to delete: ")
            if todo.delete_task(task_id):
                print(f"🗑️ Task {task_id} deleted successfully!")
            else:
                print(f"❌ Task with ID {task_id} not found.")
        
        elif choice == '5':
            todo.list_tasks(show_completed=False)
        
        elif choice == '6':
            confirm = input("\n⚠️ Are you sure you want to delete ALL tasks? (y/n): ").lower()
            if confirm in ['y', 'yes']:
                todo.tasks.clear()
                todo.next_id = 1
                todo.save_tasks()
                print("🧹 All tasks have been cleared.")
            else:
                print("🗑️ Clear operation cancelled.")
        
        elif choice == '7':
            print("\n💾 Saving tasks and exiting...")
            todo.save_tasks()
            print("\n👋 Thank you for using the To-Do List Application!")
            print("   Stay productive! 🚀")
            time.sleep(1)
            break
        
        else:
            print("❌ Invalid choice. Please enter a number between 1 and 7.")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! Tasks have been saved.")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")