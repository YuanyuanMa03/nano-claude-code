"""Tests for dispatcher module."""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from dispatcher import ToolDispatcher


class TestToolDispatcher:
    """Test cases for ToolDispatcher."""

    def test_dispatcher_initialization(self):
        """Test dispatcher initialization."""
        dispatcher = ToolDispatcher()
        assert dispatcher.handlers == {}
        assert dispatcher.list_tools() == []

    def test_register_tool(self):
        """Test registering a tool."""
        dispatcher = ToolDispatcher()

        def dummy_handler(**kwargs):
            return "dummy result"

        dispatcher.register("dummy", dummy_handler)
        assert "dummy" in dispatcher.list_tools()
        assert dispatcher.handlers["dummy"] == dummy_handler

    def test_execute_tool(self):
        """Test executing a tool."""
        dispatcher = ToolDispatcher()

        def echo_handler(**kwargs):
            return kwargs.get("message", "default")

        dispatcher.register("echo", echo_handler)
        result = dispatcher.execute("echo", message="hello")
        assert result == "hello"

    def test_execute_unknown_tool(self):
        """Test executing an unknown tool."""
        dispatcher = ToolDispatcher()
        result = dispatcher.execute("unknown_tool")
        assert "Error: Unknown tool" in result
        assert "unknown_tool" in result

    def test_execute_batch(self):
        """Test batch execution of tools."""
        dispatcher = ToolDispatcher()

        def echo_handler(**kwargs):
            return kwargs.get("value", "default")

        dispatcher.register("echo", echo_handler)

        calls = [
            {"name": "echo", "id": "1", "input": {"value": "first"}},
            {"name": "echo", "id": "2", "input": {"value": "second"}},
        ]

        results = dispatcher.execute_batch(calls)

        assert len(results) == 2
        assert results[0]["id"] == "1"
        assert results[0]["content"] == "first"
        assert results[1]["id"] == "2"
        assert results[1]["content"] == "second"

    def test_execute_batch_with_unknown_tool(self):
        """Test batch execution with unknown tool."""
        dispatcher = ToolDispatcher()

        calls = [
            {"name": "unknown", "id": "1", "input": {}},
        ]

        results = dispatcher.execute_batch(calls)

        assert len(results) == 1
        assert "Error: Unknown tool" in results[0]["content"]

    def test_handler_exception_handling(self):
        """Test that exceptions in handlers are caught."""
        dispatcher = ToolDispatcher()

        def failing_handler(**kwargs):
            raise ValueError("Intentional error")

        dispatcher.register("failing", failing_handler)
        result = dispatcher.execute("failing")
        assert "Error executing failing" in result
