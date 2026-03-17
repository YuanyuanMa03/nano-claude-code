"""Bash tool implementation for v01 minimal loop."""

import subprocess
from typing import Optional


def run_bash(command: str, timeout: int = 120) -> str:
    """
    Execute a bash command and return the output.

    Args:
        command: The command to execute
        timeout: Maximum time to wait for command completion (default: 120s)

    Returns:
        The combined stdout and stderr from the command
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            timeout=timeout,
            capture_output=True,
            text=True,
        )
        output = result.stdout
        if result.stderr:
            output += "\n" + result.stderr
        return output
    except subprocess.TimeoutExpired:
        return f"Error: Command timed out after {timeout} seconds"
    except Exception as e:
        return f"Error: {str(e)}"
