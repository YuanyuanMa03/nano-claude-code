"""Path security sandbox for v02 tool system."""

from pathlib import Path
from typing import Union


class SecuritySandbox:
    """
    Security sandbox for path operations.

    Prevents path traversal attacks and ensures all file operations
    stay within the designated workspace directory.

    Security features:
    - Path traversal prevention (../)
    - Absolute path restrictions
    - Symlink protection
    """

    def __init__(self, workspace: Union[str, Path]):
        """
        Initialize the sandbox with a workspace directory.

        Args:
            workspace: Root directory for all file operations
        """
        self.workspace = Path(workspace).resolve()

    def safe_path(self, path: str) -> Path:
        """
        Get a safe, absolute path within the workspace.

        Args:
            path: User-provided path (relative or absolute)

        Returns:
            Absolute path within workspace

        Raises:
            ValueError: If path escapes workspace
        """
        # Convert to absolute path
        if Path(path).is_absolute():
            # Absolute path - must be within workspace
            full_path = Path(path).resolve()
        else:
            # Relative path - join with workspace
            full_path = (self.workspace / path).resolve()

        # Verify path is within workspace
        if not full_path.is_relative_to(self.workspace):
            raise ValueError(
                f"Path escapes workspace: {path}\n"
                f"Resolved to: {full_path}\n"
                f"Workspace: {self.workspace}"
            )

        return full_path

    def check_write_permission(self, path: str) -> bool:
        """
        Check if write operation is allowed for this path.

        Args:
            path: Path to check

        Returns:
            True if write is allowed
        """
        try:
            safe = self.safe_path(path)
            # Don't allow writing to parent directories
            if safe == self.workspace:
                return False
            return True
        except ValueError:
            return False

    def normalize_path(self, path: str) -> str:
        """
        Normalize a path for display purposes.

        Args:
            path: Path to normalize

        Returns:
            Normalized path string
        """
        try:
            safe = self.safe_path(path)
            # Try to make it relative to workspace for cleaner display
            try:
                return str(safe.relative_to(self.workspace))
            except ValueError:
                # Can't make relative, return absolute
                return str(safe)
        except ValueError:
            # Path is unsafe, return as-is for error messages
            return path
