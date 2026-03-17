"""Todo write tool for v03 task planning."""

from typing import List, Dict, Any

try:
    from .todo_manager import TodoManager
except ImportError:
    from todo_manager import TodoManager


def create_todo_tool(todo_manager: TodoManager) -> dict:
    """
    Create a todo tool handler for the dispatcher.

    Args:
        todo_manager: TodoManager instance

    Returns:
        Dictionary with tool name and handler
    """
    def todo_write_handler(**kwargs) -> str:
        """
        Handle TodoWrite tool calls.

        Args:
            items: List of todo item dictionaries

        Returns:
            Rendered todo list
        """
        items = kwargs.get("items", [])

        if not isinstance(items, list):
            return "Error: 'items' must be a list"

        # Validate each item
        for i, item in enumerate(items):
            if not isinstance(item, dict):
                return f"Error: Item {i} is not a dictionary"

            if "id" not in item or "text" not in item:
                return f"Error: Item {i} missing required fields 'id' or 'text'"

            if "status" in item and item["status"] not in ["pending", "in_progress", "completed"]:
                return f"Error: Item {i} has invalid status '{item['status']}'"

        try:
            return todo_manager.update(items)
        except ValueError as e:
            return f"Error: {e}"

    return {
        "name": "todo_write",
        "handler": todo_write_handler
    }


def get_todo_schema() -> Dict[str, Any]:
    """
    Get the JSON schema for the TodoWrite tool.

    Returns:
        Tool schema dictionary
    """
    return {
        "name": "todo_write",
        "description": "Update the task list. Call this frequently to track progress.",
        "input_schema": {
            "type": "object",
            "properties": {
                "items": {
                    "type": "array",
                    "description": "List of todo items",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "Unique identifier for the task"
                            },
                            "text": {
                                "type": "string",
                                "description": "Task description"
                            },
                            "status": {
                                "type": "string",
                                "enum": ["pending", "in_progress", "completed"],
                                "description": "Task status"
                            }
                        },
                        "required": ["id", "text"]
                    }
                }
            },
            "required": ["items"]
        }
    }
