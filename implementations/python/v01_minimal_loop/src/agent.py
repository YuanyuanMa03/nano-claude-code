"""Minimal agent loop implementation for v01."""

import os
from typing import List, Dict, Any

try:
    from anthropic import Anthropic
except ImportError:
    raise ImportError(
        "Please install anthropic: pip install anthropic"
    )

from bash_tool import run_bash


class AgentLoop:
    """
    Minimal agent loop that:
    1. Sends messages to LLM
    2. Checks stop_reason
    3. Executes bash tool if needed
    4. Loops back to step 1
    """

    def __init__(self, api_key: str, model: str = "claude-sonnet-4-6"):
        """
        Initialize the agent loop.

        Args:
            api_key: Anthropic API key
            model: Model to use (default: claude-sonnet-4-6)
        """
        self.client = Anthropic(api_key=api_key)
        self.model = model

        # Define the bash tool schema
        self.tools = [{
            "name": "bash",
            "description": "Execute a bash command in the terminal",
            "input_schema": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The command to execute"
                    },
                    "timeout": {
                        "type": "integer",
                        "description": "Maximum time to wait in seconds",
                        "default": 120
                    }
                },
                "required": ["command"]
            }
        }]

    def run(self, user_query: str) -> str:
        """
        Run the agent loop with a user query.

        Args:
            user_query: The user's input query

        Returns:
            The final response from the agent
        """
        messages = [{
            "role": "user",
            "content": user_query
        }]

        while True:
            # Call LLM
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                messages=messages,
                tools=self.tools,
            )

            # Add assistant response to messages
            messages.append({
                "role": "assistant",
                "content": response.content
            })

            # Check if we need to use tools
            if response.stop_reason != "tool_use":
                # Extract text content from final response
                final_text = self._extract_text(response.content)
                return final_text

            # Execute tool calls
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = self._execute_tool(block.name, block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    })

            # Add tool results to messages
            messages.append({
                "role": "user",
                "content": tool_results
            })

    def _extract_text(self, content: List[Any]) -> str:
        """Extract text content from response blocks."""
        text_parts = []
        for block in content:
            if block.type == "text":
                text_parts.append(block.text)
        return "\n".join(text_parts)

    def _execute_tool(self, tool_name: str, tool_input: Dict[str, Any]) -> str:
        """Execute a tool by name."""
        if tool_name == "bash":
            command = tool_input.get("command", "")
            timeout = tool_input.get("timeout", 120)
            return run_bash(command, timeout)
        else:
            return f"Error: Unknown tool '{tool_name}'"
