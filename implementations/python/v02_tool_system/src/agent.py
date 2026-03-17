"""Agent loop for v02 tool system."""

import os
from typing import List, Dict, Any

try:
    from anthropic import Anthropic
except ImportError:
    raise ImportError("Please install anthropic: pip install anthropic")

try:
    from .dispatcher import ToolDispatcher
    from .file_tools import create_file_tools
except ImportError:
    from dispatcher import ToolDispatcher
    from file_tools import create_file_tools


def run_bash(command: str, timeout: int = 120) -> str:
    """Execute bash command."""
    import subprocess
    try:
        result = subprocess.run(
            command,
            shell=True,
            timeout=timeout,
            capture_output=True,
            text=True
        )
        output = result.stdout or result.stderr
        return output
    except subprocess.TimeoutExpired:
        return f"Command timed out after {timeout} seconds"
    except Exception as e:
        return f"Error: {e}"


class AgentLoop:
    """
    Agent loop with tool dispatcher system.

    Motto: "Adding a tool means adding one handler"

    This version introduces:
    - ToolDispatcher for routing tool calls
    - File operations (read_file, write_file, edit_file)
    - Path security sandbox
    """

    def __init__(self, api_key: str, model: str = "claude-sonnet-4-6", workspace: str = "."):
        """
        Initialize the agent loop.

        Args:
            api_key: Anthropic API key
            model: Model to use
            workspace: Workspace directory for file operations
        """
        self.client = Anthropic(api_key=api_key)
        self.model = model
        self.workspace = os.path.abspath(workspace)

        # Initialize tool dispatcher
        self.dispatcher = ToolDispatcher()

        # Register bash tool
        self.dispatcher.register("bash", lambda **kw: run_bash(
            kw.get("command", ""),
            kw.get("timeout", 120)
        ))

        # Register file tools
        file_tools = create_file_tools(self.workspace)
        for name, handler in file_tools.items():
            self.dispatcher.register(name, handler)

        # Define tool schemas for LLM
        self.tools = [
            {
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
            },
            {
                "name": "read_file",
                "description": "Read the contents of a file",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "File path to read"
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of lines to read"
                        }
                    },
                    "required": ["path"]
                }
            },
            {
                "name": "write_file",
                "description": "Write content to a file",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "File path to write"
                        },
                        "content": {
                            "type": "string",
                            "description": "Content to write to the file"
                        }
                    },
                    "required": ["path", "content"]
                }
            },
            {
                "name": "edit_file",
                "description": "Edit a file by replacing text",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "File path to edit"
                        },
                        "old_text": {
                            "type": "string",
                            "description": "Text to replace"
                        },
                        "new_text": {
                            "type": "string",
                            "description": "Replacement text"
                        }
                    },
                    "required": ["path", "old_text", "new_text"]
                }
            }
        ]

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
            tool_calls = []
            for block in response.content:
                if block.type == "tool_use":
                    tool_calls.append({
                        "name": block.name,
                        "id": block.id,
                        "input": block.input
                    })

            # Use dispatcher to execute tools
            tool_results = self.dispatcher.execute_batch(tool_calls)

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

    def list_tools(self) -> List[str]:
        """List all registered tools."""
        return self.dispatcher.list_tools()
