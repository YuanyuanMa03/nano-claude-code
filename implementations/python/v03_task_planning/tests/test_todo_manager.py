"""Tests for todo_manager module."""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from todo_manager import TodoManager, TodoItem


class TestTodoItem:
    """Test cases for TodoItem."""

    def test_todo_item_creation(self):
        """Test creating a todo item."""
        item = TodoItem(
            id="1",
            text="Test task"
        )
        assert item.id == "1"
        assert item.text == "Test task"
        assert item.status == "pending"

    def test_todo_item_to_dict(self):
        """Test converting todo item to dictionary."""
        item = TodoItem(
            id="1",
            text="Test task",
            status="in_progress"
        )
        data = item.to_dict()
        assert data["id"] == "1"
        assert data["text"] == "Test task"
        assert data["status"] == "in_progress"
        assert "created_at" in data

    def test_todo_item_from_dict(self):
        """Test creating todo item from dictionary."""
        data = {
            "id": "1",
            "text": "Test task",
            "status": "completed"
        }
        item = TodoItem.from_dict(data)
        assert item.id == "1"
        assert item.text == "Test task"
        assert item.status == "completed"

    def test_todo_item_from_dict_default_status(self):
        """Test creating todo item with default status."""
        data = {
            "id": "1",
            "text": "Test task"
        }
        item = TodoItem.from_dict(data)
        assert item.status == "pending"


class TestTodoManager:
    """Test cases for TodoManager."""

    def test_manager_initialization(self):
        """Test manager initialization."""
        manager = TodoManager()
        assert manager.items == []
        assert manager.nag_counter == 0

    def test_update_with_valid_items(self):
        """Test updating with valid todo items."""
        manager = TodoManager()
        items = [
            {"id": "1", "text": "Task 1", "status": "pending"},
            {"id": "2", "text": "Task 2", "status": "in_progress"}
        ]
        result = manager.update(items)
        assert "Task 1" in result
        assert "Task 2" in result
        assert len(manager.items) == 2

    def test_update_multiple_in_progress_raises_error(self):
        """Test that multiple in_progress tasks raise error."""
        manager = TodoManager()
        items = [
            {"id": "1", "text": "Task 1", "status": "in_progress"},
            {"id": "2", "text": "Task 2", "status": "in_progress"}
        ]
        with pytest.raises(ValueError, match="Only one task can be in_progress"):
            manager.update(items)

    def test_update_resets_nag_counter(self):
        """Test that updating resets the nag counter."""
        manager = TodoManager()
        manager.nag_counter = 5

        items = [{"id": "1", "text": "Task 1"}]
        manager.update(items)

        assert manager.nag_counter == 0

    def test_render_empty_list(self):
        """Test rendering empty todo list."""
        manager = TodoManager()
        result = manager.render()
        assert result == "No tasks"

    def test_render_with_items(self):
        """Test rendering todo list with items."""
        manager = TodoManager()
        items = [
            {"id": "1", "text": "Pending task", "status": "pending"},
            {"id": "2", "text": "In progress task", "status": "in_progress"},
            {"id": "3", "text": "Completed task", "status": "completed"}
        ]
        manager.update(items)
        result = manager.render()
        assert "⬜" in result
        assert "🔄" in result
        assert "✅" in result
        assert "Pending task" in result
        assert "In progress task" in result
        assert "Completed task" in result

    def test_should_nag(self):
        """Test nag counter mechanism."""
        manager = TodoManager()

        # First two calls should not nag
        assert not manager.should_nag()
        assert not manager.should_nag()

        # Third call should nag
        assert manager.should_nag()

    def test_get_progress_empty(self):
        """Test progress calculation with empty list."""
        manager = TodoManager()
        progress = manager.get_progress()
        assert progress == 0.0

    def test_get_progress(self):
        """Test progress calculation."""
        manager = TodoManager()
        items = [
            {"id": "1", "text": "Task 1", "status": "completed"},
            {"id": "2", "text": "Task 2", "status": "pending"},
            {"id": "3", "text": "Task 3", "status": "completed"}
        ]
        manager.update(items)
        progress = manager.get_progress()
        assert progress == 2/3

    def test_get_stats(self):
        """Test getting statistics."""
        manager = TodoManager()
        items = [
            {"id": "1", "text": "Task 1", "status": "pending"},
            {"id": "2", "text": "Task 2", "status": "in_progress"},
            {"id": "3", "text": "Task 3", "status": "completed"},
            {"id": "4", "text": "Task 4", "status": "completed"}
        ]
        manager.update(items)
        stats = manager.get_stats()
        assert stats["pending"] == 1
        assert stats["in_progress"] == 1
        assert stats["completed"] == 2
        assert stats["total"] == 4

    def test_to_dict_list(self):
        """Test converting items to dict list."""
        manager = TodoManager()
        items = [
            {"id": "1", "text": "Task 1"}
        ]
        manager.update(items)
        dict_list = manager.to_dict_list()
        assert len(dict_list) == 1
        assert dict_list[0]["id"] == "1"
        assert dict_list[0]["text"] == "Task 1"
