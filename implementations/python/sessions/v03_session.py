#!/usr/bin/env python3
"""
v03_session.py - Task Planning Session

**Motto**: "An agent without a plan drifts"

This session demonstrates the task planning pattern:
    - TodoWrite tool for task management
    - Single task in_progress constraint
    - Automatic reminder mechanism

+--------+      +-------------+      +-----------+
|  User  | ---> | TodoManager | ---> | Constraint |
| request|      |  tracks     |      | enforcement|
+--------+      +-------------+      +-----------+
                      ^
                      | one in_progress
                      +-----------------

Learning Goals:
- Understand why task planning matters
- Learn the single-task constraint pattern
- See how reminders prevent drift
- Learn to extend the agent system

Usage:
    ANTHROPIC_API_KEY=xxx python v03_session.py
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
Use tools to solve tasks. Be concise and action-oriented.

IMPORTANT: Always use the TodoWrite tool to plan your tasks before starting work.
Update your todos frequently to track progress.
Only ONE task can be in progress at a time."""

# ============================================
# V03: Task Planning Pattern
# ============================================
# The key insight: agents need plans to stay focused
#
# Problem: Without a plan, agents tend to:
#   - Repeat work
#   - Skip steps
#   - Get sidetracked
#   - Forget what they were doing
#
# Solution: TodoManager with:
#   - List of tasks with status
#   - Constraint: only ONE in_progress
#   - Auto-reminder after 3 rounds
# ============================================

from dataclasses import dataclass
from typing import List

@dataclass
class TodoItem:
    """A single todo item."""
    id: str
    text: str
    status: str = "pending"  # pending, in_progress, completed

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "status": self.status
        }


class TodoManager:
    """Motto: An agent without a plan drifts"""

    STATUS_EMOJI = {
        "pending": "⬜",
        "in_progress": "🔄",
        "completed": "✅"
    }

    def __init__(self):
        self.items: List[TodoItem] = []
        self.nag_counter = 0

    def update(self, items_dict: List[dict]) -> str:
        """Update todo list with validation."""
        items = [TodoItem(**i) for i in items_dict]

        # KEY CONSTRAINT: Only one in_progress
        in_progress = sum(1 for i in items if i.status == "in_progress")
        if in_progress > 1:
            raise ValueError("Only one task can be in_progress!")

        self.items = items
        self.nag_counter = 0  # Reset on update
        return self.render()

    def render(self) -> str:
        """Render todos as formatted string."""
        if not self.items:
            return "No tasks"

        lines = []
        for item in self.items:
            emoji = self.STATUS_EMOJI.get(item.status, "❓")
            lines.append(f"{emoji} {item.text}")
        return "\n".join(lines)

    def should_nag(self) -> bool:
        """Check if we should remind the agent."""
        self.nag_counter += 1
        return self.nag_counter >= 3

    def get_progress(self) -> float:
        """Get completion ratio."""
        if not self.items:
            return 0.0
        completed = sum(1 for i in self.items if i.status == "completed")
        return completed / len(self.items)


# ============================================
# Tool Dispatcher (from v02)
# ============================================

class ToolDispatcher:
    """Simple tool dispatcher."""
    def __init__(self):
        self.handlers = {}

    def register(self, name: str, handler):
        self.handlers[name] = handler

    def execute(self, name: str, **kwargs):
        handler = self.handlers.get(name)
        if not handler:
            return f"Error: Unknown tool '{name}'"
        return handler(**kwargs)

    def execute_batch(self, calls: List[dict]) -> List[dict]:
        results = []
        for call in calls:
            output = self.execute(call["name"], **call["input"])
            results.append({"id": call["id"], "content": output})
        return results


# ============================================
# Tool Handlers
# ============================================

dispatcher = ToolDispatcher()

# Bash tool
def run_bash(command: str) -> str:
    try:
        result = subprocess.run(
            command, shell=True, timeout=120,
            capture_output=True, text=True
        )
        return result.stdout or result.stderr
    except subprocess.TimeoutExpired:
        return "Command timed out"
    except Exception as e:
        return f"Error: {e}"

dispatcher.register("bash", run_bash)

# File tools (simplified for session)
def read_file(path: str) -> str:
    try:
        with open(path, 'r') as f:
            return f.read()
    except Exception as e:
        return f"Error: {e}"

def write_file(path: str, content: str) -> str:
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write(content)
        return f"Wrote {len(content)} bytes"
    except Exception as e:
        return f"Error: {e}"

dispatcher.register("read_file", read_file)
dispatcher.register("write_file", write_file)

# Todo tool
def todo_write(**kwargs) -> str:
    items = kwargs.get("items", [])
    if not isinstance(items, list):
        return "Error: items must be a list"

    todo_items = [TodoItem(**i) for i in items]
    return todo_manager.update([i.to_dict() for i in todo_items])

dispatcher.register("todo_write", todo_write)

# Tool schemas
TOOLS = [
    {
        "name": "bash",
        "description": "Execute shell command",
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
                "path": {"type": "string"}
            },
            "required": ["path"]
        }
    },
    {
        "name": "write_file",
        "description": "Write to file",
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
        "name": "todo_write",
        "description": "Update task list. Call frequently!",
        "input_schema": {
            "type": "object",
            "properties": {
                "items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "text": {"type": "string"},
                            "status": {
                                "type": "string",
                                "enum": ["pending", "in_progress", "completed"]
                            }
                        },
                        "required": ["id", "text"]
                    }
                }
            },
            "required": ["items"]
        }
    }
]


def agent_loop(user_query: str) -> str:
    """Agent loop with task planning."""
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

        # Execute tools
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                print(f"[Tool: {block.name}]")
                if block.name == "todo_write":
                    # Show todos more clearly
                    items = block.input.get("items", [])
                    print("  Tasks:")
                    for item in items:
                        status = item.get("status", "pending")
                        emoji = {"pending": "⬜", "in_progress": "🔄", "completed": "✅"}[status]
                        print(f"    {emoji} {item.get('text', 'No text')}")
                elif block.name == "write_file":
                    print(f"  Path: {block.input.get('path')}")
                    print(f"  Content: {block.input.get('content', '')[:50]}...")
                else:
                    for key, value in block.input.items():
                        if key != "content":
                            print(f"  {key}: {value}")
                print()

                output = dispatcher.execute(block.name, **block.input)
                print(f"Result: {output[:100]}...")
                print()

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": output
                })

        # Add reminder if needed
        if todo_manager.should_nag():
            print("💡 <reminder> Please update your todos!")
            if tool_results:
                tool_results[-1]["content"] += "\n\n<reminder>Please update your todos.</reminder>"

        messages.append({"role": "user", "content": tool_results})


def main():
    """Interactive session."""
    print("=" * 60)
    print("v03 Session - Task Planning")
    print("=" * 60)
    print("\nMotto: \"An agent without a plan drifts\"")
    print(f"\nWorkspace: {os.path.abspath(WORKSPACE)}")
    print("\nThis session demonstrates task planning for agents.")
    print("Key features:")
    print("  • TodoWrite tool for task management")
    print("  • Single task in_progress constraint")
    print("  • Automatic reminder mechanism")
    print("\nType 'exit' to quit\n")

    # Example tasks
    examples = [
        "Plan and implement a simple calculator",
        "Refactor the code to add type hints",
        "Create a test suite for the project"
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

            # Show progress if any todos
            if todo_manager.items:
                progress = todo_manager.get_progress()
                stats = todo_manager.get_stats()
                print(f"\n[Todo Progress: {progress*100:.0f}% - {stats['completed']}/{stats['total']} completed]")
                print()

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}\n")


if __name__ == "__main__":
    # Create todo manager instance
    todo_manager = TodoManager()
    main()
