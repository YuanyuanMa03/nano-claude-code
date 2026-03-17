#!/usr/bin/env python3
"""
v01_session.py - Minimal Loop Session

**Motto**: "One loop & Bash is all you need"

This session demonstrates the core agent loop pattern:
    while stop_reason == "tool_use":
        response = LLM(messages, tools)
        execute tools
        append results

+----------+      +-------+      +---------+
|   User   | ---> |  LLM  | ---> |  Tool   |
|  prompt  |      |       |      | execute |
+----------+      +---+---+      +----+----+
                      ^               |
                      |   tool_result |
                      +---------------+
                      (loop continues)

Learning Goals:
- Understand the stop_reason mechanism
- See how tool results feed back into the loop
- Implement the minimal viable agent

Usage:
    ANTHROPIC_API_KEY=xxx python v01_session.py
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

# Remove auth token if using custom base URL
if BASE_URL:
    os.environ.pop("ANTHROPIC_AUTH_TOKEN", None)

client = Anthropic(api_key=API_KEY, base_url=BASE_URL)

# Simple system prompt
SYSTEM = f"""You are a coding agent working in {os.getcwd()}.
Use bash to solve tasks. Be concise and action-oriented."""

# Define bash tool
TOOLS = [{
    "name": "bash",
    "description": "Execute shell commands",
    "input_schema": {
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "description": "Command to execute"
            }
        },
        "required": ["command"]
    }
}]

def run_bash(command: str) -> str:
    """Execute bash command and return output."""
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

def agent_loop(user_query: str) -> str:
    """
    Core agent loop - the heart of every AI agent.

    This loop continues until the model decides to stop using tools.
    """
    messages = [{"role": "user", "content": user_query}]

    while True:
        # Call LLM with current messages and tool definitions
        response = client.messages.create(
            model=MODEL,
            max_tokens=4096,
            system=SYSTEM,
            messages=messages,
            tools=TOOLS,
        )

        # Add assistant response to message history
        messages.append({"role": "assistant", "content": response.content})

        # KEY: Check why the model stopped
        if response.stop_reason != "tool_use":
            # Model is done - extract and return final text
            text_parts = []
            for block in response.content:
                if block.type == "text":
                    text_parts.append(block.text)
            return "\n".join(text_parts)

        # Model wants to use tools - execute them
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                print(f"[Tool: {block.name}]")
                print(f"Command: {block.input.get('command', '')}")

                output = run_bash(block.input.get("command", ""))
                print(f"Result: {output[:200]}...")
                print()

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": output
                })

        # Add tool results to messages and loop back
        messages.append({"role": "user", "content": tool_results})

def main():
    """Interactive session."""
    print("=" * 60)
    print("v01 Session - Minimal Loop")
    print("=" * 60)
    print("\nThis session demonstrates the core agent loop.")
    print("Type 'exit' to quit\n")

    # Example task to try
    example_task = "Create a file called hello.py with a simple function"

    print(f"Example task: {example_task}")
    print(f"Try it or type your own!\n")

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
