"""Tool dispatcher for v02 tool system."""

from typing import Dict, Callable, Any, List
from pathlib import Path


class ToolDispatcher:
    """
    Tool dispatcher - Adding a tool means adding one handler.

    The dispatcher routes tool calls to the appropriate handler function.
    Each tool is registered with a name and a handler function.

    Motto: "Adding a tool means adding one handler"

    Example:
        dispatcher = ToolDispatcher()

        # Register tools
        dispatcher.register("bash", bash_handler)
        dispatcher.register("read_file", read_handler)

        # Execute tools
        result = dispatcher.execute("bash", command="ls")
    """

    def __init__(self):
        """Initialize the tool dispatcher."""
        self.handlers: Dict[str, Callable] = {}

    def register(self, name: str, handler: Callable):
        """
        Register a tool handler.

        Args:
            name: Tool name
            handler: Function that executes the tool

        Example handler:
            def my_handler(**kwargs) -> str:
                # Process kwargs
                return "result"
        """
        self.handlers[name] = handler

    def execute(self, name: str, **kwargs) -> str:
        """
        Execute a tool by name.

        Args:
            name: Tool name to execute
            **kwargs: Tool arguments

        Returns:
            Tool output as string

        Raises:
            ValueError: If tool not found
        """
        handler = self.handlers.get(name)
        if not handler:
            return f"Error: Unknown tool '{name}'"

        try:
            return handler(**kwargs)
        except Exception as e:
            return f"Error executing {name}: {e}"

    def execute_batch(self, calls: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Execute multiple tools in batch.

        Args:
            calls: List of tool calls with 'name' and 'input' keys

        Returns:
            List of tool results with 'id', 'content', and optionally 'error'
        """
        results = []
        for call in calls:
            tool_name = call.get("name")
            tool_id = call.get("id")
            tool_input = call.get("input", {})

            output = self.execute(tool_name, **tool_input)

            results.append({
                "id": tool_id,
                "content": output
            })

        return results

    def get_schemas(self) -> List[Dict[str, Any]]:
        """
        Get all tool schemas for LLM.

        This method should be overridden or tools should register
        their schemas. For now, returns empty list.

        Returns:
            List of tool schemas
        """
        # Tools will need to register their schemas
        # This is a placeholder for future enhancement
        return []

    def list_tools(self) -> List[str]:
        """
        List all registered tool names.

        Returns:
            List of tool names
        """
        return list(self.handlers.keys())
