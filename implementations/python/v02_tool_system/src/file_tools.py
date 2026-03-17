"""File operation tools for v02 tool system."""

import os
from pathlib import Path
from typing import Optional

try:
    from .sandbox import SecuritySandbox
except ImportError:
    from sandbox import SecuritySandbox


class FileTools:
    """
    File operation tools with path security.

    Provides read_file, write_file, and edit_file tools
    with sandbox path protection.
    """

    def __init__(self, workspace: str):
        """
        Initialize file tools with workspace directory.

        Args:
            workspace: Root directory for file operations
        """
        self.sandbox = SecuritySandbox(workspace)

    def read_file(self, path: str, limit: Optional[int] = None) -> str:
        """
        Read file contents.

        Args:
            path: File path (relative to workspace)
            limit: Maximum number of lines to read (optional)

        Returns:
            File contents as string
        """
        try:
            safe_path = self.sandbox.safe_path(path)

            if not safe_path.exists():
                return f"Error: File not found: {path}"

            if not safe_path.is_file():
                return f"Error: Not a file: {path}"

            with open(safe_path, 'r', encoding='utf-8') as f:
                if limit:
                    lines = []
                    for i, line in enumerate(f):
                        if i >= limit:
                            break
                        lines.append(line)
                    content = ''.join(lines)
                else:
                    content = f.read()

            # Limit output size
            max_size = 50000  # 50KB limit
            if len(content) > max_size:
                content = content[:max_size] + f"\n... (truncated, total {len(content)} bytes)"

            return content

        except ValueError as e:
            return f"Error: {e}"
        except Exception as e:
            return f"Error reading file: {e}"

    def write_file(self, path: str, content: str) -> str:
        """
        Write content to a file.

        Args:
            path: File path (relative to workspace)
            content: Content to write

        Returns:
            Success message
        """
        try:
            if not self.sandbox.check_write_permission(path):
                return f"Error: Cannot write to {path}"

            safe_path = self.sandbox.safe_path(path)

            # Create parent directories if needed
            safe_path.parent.mkdir(parents=True, exist_ok=True)

            with open(safe_path, 'w', encoding='utf-8') as f:
                f.write(content)

            return f"Successfully wrote {len(content)} bytes to {path}"

        except ValueError as e:
            return f"Error: {e}"
        except Exception as e:
            return f"Error writing file: {e}"

    def edit_file(self, path: str, old_text: str, new_text: str) -> str:
        """
        Edit file by replacing old_text with new_text.

        Args:
            path: File path (relative to workspace)
            old_text: Text to replace
            new_text: Replacement text

        Returns:
            Success message
        """
        try:
            if not self.sandbox.check_write_permission(path):
                return f"Error: Cannot edit {path}"

            safe_path = self.sandbox.safe_path(path)

            if not safe_path.exists():
                return f"Error: File not found: {path}"

            with open(safe_path, 'r', encoding='utf-8') as f:
                content = f.read()

            if old_text not in content:
                return f"Error: '{old_text[:50]}...' not found in {path}"

            # Replace only first occurrence
            new_content = content.replace(old_text, new_text, 1)

            with open(safe_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            return f"Successfully replaced text in {path}"

        except ValueError as e:
            return f"Error: {e}"
        except Exception as e:
            return f"Error editing file: {e}"


def create_file_tools(workspace: str) -> dict:
    """
    Create file tool handlers for the dispatcher.

    Args:
        workspace: Workspace directory

    Returns:
        Dictionary of tool name to handler function
    """
    file_tools = FileTools(workspace)

    return {
        "read_file": lambda **kwargs: file_tools.read_file(
            kwargs.get("path", ""),
            kwargs.get("limit")
        ),
        "write_file": lambda **kwargs: file_tools.write_file(
            kwargs.get("path", ""),
            kwargs.get("content", "")
        ),
        "edit_file": lambda **kwargs: file_tools.edit_file(
            kwargs.get("path", ""),
            kwargs.get("old_text", ""),
            kwargs.get("new_text", "")
        ),
    }
