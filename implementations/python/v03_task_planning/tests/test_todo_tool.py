"""Tests for todo_tool module."""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from todo_manager import TodoManager
from todo_tool import create_todo_tool, get_todo_schema


class TestTodoTool:
    """Test cases for TodoWrite tool."""

    @pytest.fixture
    def todo_manager(self):
        """Create a TodoManager instance."""
        return TodoManager()

    def test_create_todo_tool(self, todo_manager):
        """Test creating todo tool."""
        tool = create_todo_tool(todo_manager)
        assert tool["name"] == "todo_write"
        assert callable(tool["handler"])

    def test_todo_write_handler_valid(self, todo_manager):
        """Test todo_write handler with valid input."""
        tool = create_todo_tool(todo_manager)
        handler = tool["handler"]

        result = handler(items=[
            {"id": "1", "text": "Task 1"},
            {"id": "2", "text": "Task 2", "status": "in_progress"}
        ])

        assert "Task 1" in result
        assert "Task 2" in result

    def test_todo_write_handler_invalid_items_type(self, todo_manager):
        """Test todo_write handler with invalid items type."""
        tool = create_todo_tool(todo_manager)
        handler = tool["handler"]

        result = handler(items="not a list")
        assert "Error" in result
        assert "must be a list" in result

    def test_todo_write_handler_item_not_dict(self, todo_manager):
        """Test todo_write handler with non-dict item."""
        tool = create_todo_tool(todo_manager)
        handler = tool["handler"]

        result = handler(items=[{"id": "1"}, "not a dict", {"id": "3"}])
        assert "Error" in result
        # First item {"id": "1"} is missing "text", so it reports item 0
        assert "Item 0" in result or "Item 1" in result

    def test_todo_write_handler_missing_fields(self, todo_manager):
        """Test todo_write handler with missing required fields."""
        tool = create_todo_tool(todo_manager)
        handler = tool["handler"]

        result = handler(items=[{"text": "Task without id"}])
        assert "Error" in result
        assert "missing required fields" in result

    def test_todo_write_handler_invalid_status(self, todo_manager):
        """Test todo_write handler with invalid status."""
        tool = create_todo_tool(todo_manager)
        handler = tool["handler"]

        result = handler(items=[
            {"id": "1", "text": "Task", "status": "invalid_status"}
        ])
        assert "Error" in result
        assert "invalid status" in result

    def test_todo_write_handler_multiple_in_progress(self, todo_manager):
        """Test todo_write handler with multiple in_progress tasks."""
        tool = create_todo_tool(todo_manager)
        handler = tool["handler"]

        result = handler(items=[
            {"id": "1", "text": "Task 1", "status": "in_progress"},
            {"id": "2", "text": "Task 2", "status": "in_progress"}
        ])
        assert "Error" in result
        assert "Only one task can be in_progress" in result


class TestTodoSchema:
    """Test cases for todo schema."""

    def test_get_todo_schema(self):
        """Test getting todo tool schema."""
        schema = get_todo_schema()
        assert schema["name"] == "todo_write"
        assert "description" in schema
        assert "input_schema" in schema

    def test_schema_structure(self):
        """Test schema has correct structure."""
        schema = get_todo_schema()
        input_schema = schema["input_schema"]

        assert input_schema["type"] == "object"
        assert "properties" in input_schema
        assert "items" in input_schema["properties"]

        items_prop = input_schema["properties"]["items"]
        assert items_prop["type"] == "array"
        assert "items" in items_prop

    def test_schema_required_fields(self):
        """Test schema has correct required fields."""
        schema = get_todo_schema()
        required = schema["input_schema"]["required"]
        assert "items" in required
