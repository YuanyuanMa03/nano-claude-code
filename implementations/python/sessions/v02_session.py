#!/usr/bin/env python3
"""
v02_session.py - Tool System Session

**Motto**: "Adding a tool means adding one handler"

This session demonstrates the tool dispatcher pattern:
    dispatcher.register("tool_name", handler_function)
    result = dispatcher.execute("tool_name", **kwargs)

+--------+      +-------------+      +-----------+
|  User  | ---> |  Dispatcher | ---> |  Handler  |
| request|      |  registers  |      | executes  |
+--------+      +-------------+      +-----------+
                      ^
                      | one handler per tool
                      +----------------------

Learning Goals:
- Understand the tool dispatcher pattern
- Learn why specialized tools are better than bash
- See how path security works
- Learn to extend the system with new tools

Usage:
    ANTHROPIC_API_KEY=xxx python v02_session.py
"""

import os
import subprocess
from dotenv import load_dotenv

try:
    from anthropic import Anthropic
except ImportError:
    raise ImportError("Please install: pip install anthropic python-dotenv")

load_dotenv()

API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not API_KEY:
    raise ValueError("ANTHROPIC_API_KEY not set in .env")

MODEL = os.getenv("MODEL_ID", "claude-sonnet-4-6")
BASE_URL = os.getenv("ANTHROPIC_BASE_URL")
WORKSPACE = os.getenv("WORKSPACE", ".")

if BASE_URL:
    os.environ.pop("ANTHROPIC_AUTH_TOKEN", None)

client = Anthropic(api_key=API_KEY, base_url=BASE_URL)

SYSTEM = f"""You are a coding agent working in {os.path.abspath(WORKSPACE)}.
Use tools to solve tasks. Be concise and action-oriented."""

# ============================================
# V02: Tool Dispatcher Pattern
# ============================================
# The key insight: adding a tool means adding one handler
#
# In v01, tool execution was hardcoded:
#   if tool == "bash": run_bash()
#   else: error
#
# In v02, we use a dispatcher:
#   dispatcher.register("bash", run_bash)
#   dispatcher.register("read", read_file)
#   result = dispatcher.execute(tool_name, **kwargs)
# ============================================


class ToolDispatcher:
    """Simple tool dispatcher - routes tool calls to handlers."""

    def __init__(self):
        self.handlers = {}

    def register(self, name: str, handler):
        """Register a tool handler - one line adds a tool!"""
        self.handlers[name] = handler
        print(f"  ✓ Registered tool: {name}")

    def execute(self, name: str, **kwargs):
        """Execute a tool by calling its handler."""
        handler = self.handlers.get(name)
        if not handler:
            return f"Error: Unknown tool '{name}'"
        try:
            return handler(**kwargs)
        except Exception as e:
            return f"Error: {e}"


# ============================================
# Security Sandbox
# ============================================
# Prevents path traversal attacks like:
#   read_file("../../../etc/passwd")
# ============================================

class SecuritySandbox:
    """Ensures all file operations stay within workspace."""

    def __init__(self, workspace: str):
        self.workspace = os.path.abspath(workspace)

    def safe_path(self, path: str) -> str:
        """Get safe absolute path within workspace."""
        full = os.path.abspath(os.path.join(self.workspace, path))

        # Critical security check!
        if not full.startswith(self.workspace):
            raise ValueError(f"Path escapes workspace: {path}")

        return full


# ============================================
# Tool Handlers
# ============================================

sandbox = SecuritySandbox(WORKSPACE)


def run_bash(command: str) -> str:
    """Execute bash command."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            timeout=120,
            capture_output=True,
            text=True
        )
        return result.stdout or result.stderr
    except subprocess.TimeoutExpired:
        return "Command timed out"
    except Exception as e:
        return f"Error: {e}"


def read_file(path: str, limit: int = None) -> str:
    """Read file contents safely."""
    try:
        safe = sandbox.safe_path(path)
        with open(safe, 'r') as f:
            if limit:
                lines = [f.readline() for _ in range(limit)]
                return ''.join(lines)
            return f.read()
    except ValueError as e:
        return str(e)
    except Exception as e:
        return f"Error reading file: {e}"


def write_file(path: str, content: str) -> str:
    """Write content to file safely."""
    try:
        safe = sandbox.safe_path(path)
        os.makedirs(os.path.dirname(safe), exist_ok=True)
        with open(safe, 'w') as f:
            f.write(content)
        return f"Wrote {len(content)} bytes to {path}"
    except ValueError as e:
        return str(e)
    except Exception as e:
        return f"Error writing file: {e}"


def edit_file(path: str, old_text: str, new_text: str) -> str:
    """Edit file by replacing text."""
    try:
        safe = sandbox.safe_path(path)
        with open(safe, 'r') as f:
            content = f.read()
        if old_text not in content:
            return f"Error: '{old_text[:50]}...' not found"
        new_content = content.replace(old_text, new_text, 1)
        with open(safe, 'w') as f:
            f.write(new_content)
        return f"Replaced text in {path}"
    except ValueError as e:
        return str(e)
    except Exception as e:
        return f"Error editing file: {e}"


# ============================================
# Initialize Dispatcher
# ============================================

dispatcher = ToolDispatcher()
print("\n📦 Registering tools:")
dispatcher.register("bash", run_bash)
dispatcher.register("read_file", read_file)
dispatcher.register("write_file", write_file)
dispatcher.register("edit_file", edit_file)

# Tool schemas for LLM
TOOLS = [
    {
        "name": "bash",
        "description": "Execute shell commands",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {"type": "string"}
            },
            "required": ["command"]
        }
    },
    {
        "name": "read_file",
        "description": "Read file contents",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "limit": {"type": "integer"}
            },
            "required": ["path"]
        }
    },
    {
        "name": "write_file",
        "description": "Write content to file",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "content": {"type": "string"}
            },
            "required": ["path", "content"]
        }
    },
    {
        "name": "edit_file",
        "description": "Edit file by replacing text",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "old_text": {"type": "string"},
                "new_text": {"type": "string"}
            },
            "required": ["path", "old_text", "new_text"]
        }
    }
]


def agent_loop(user_query: str) -> str:
    """Agent loop with tool dispatcher."""
    messages = [{"role": "user", "content": user_query}]

    while True:
        response = client.messages.create(
            model=MODEL,
            max_tokens=4096,
            system=SYSTEM,
            messages=messages,
            tools=TOOLS,
        )

        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason != "tool_use":
            text_parts = []
            for block in response.content:
                if block.type == "text":
                    text_parts.append(block.text)
            return "\n".join(text_parts)

        # Execute tools via dispatcher
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                print(f"[Tool: {block.name}]")
                for key, value in block.input.items():
                    if key != "content":
                        print(f"  {key}: {value}")
                    else:
                        print(f"  {key}: {value[:50]}...")
                print()

                output = dispatcher.execute(block.name, **block.input)
                print(f"Result: {output[:100]}...")
                print()

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": output
                })

        messages.append({"role": "user", "content": tool_results})


def main():
    """Interactive session."""
    print("=" * 60)
    print("v02 Session - Tool System")
    print("=" * 60)
    print(f"\nWorkspace: {os.path.abspath(WORKSPACE)}")
    print("\nThis session demonstrates the tool dispatcher pattern.")
    print("Key insight: 'Adding a tool means adding one handler'")
    print("\nType 'exit' to quit\n")

    # Example tasks to try
    examples = [
        "Create a file called test.txt with some content",
        "Read the file test.txt",
        "Edit test.txt to add a new line",
    ]

    print("Example tasks you can try:")
    for i, ex in enumerate(examples, 1):
        print(f"  {i}. {ex}")
    print()

    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ['exit', 'quit']:
                print("\nGoodbye!")
                break

            print("\nAgent: ", end="", flush=True)
            response = agent_loop(user_input)
            print(response)
            print()

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}\n")


if __name__ == "__main__":
    main()
