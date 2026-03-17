"""Tests for sandbox module."""

import pytest
import tempfile
import shutil
import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from sandbox import SecuritySandbox


class TestSecuritySandbox:
    """Test cases for SecuritySandbox."""

    @pytest.fixture
    def temp_workspace(self):
        """Create a temporary workspace directory."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    def test_safe_path_relative(self, temp_workspace):
        """Test safe path with relative path."""
        sandbox = SecuritySandbox(temp_workspace)
        safe = sandbox.safe_path("test.txt")
        assert safe.is_absolute()
        # Resolve both to handle macOS /var -> /private symlinks
        workspace_resolved = Path(temp_workspace).resolve()
        assert safe.is_relative_to(workspace_resolved)

    def test_safe_path_absolute_within_workspace(self, temp_workspace):
        """Test safe path with absolute path within workspace."""
        sandbox = SecuritySandbox(temp_workspace)
        safe = sandbox.safe_path(str(temp_workspace))
        # Resolve both to handle symlinks
        assert safe.resolve() == Path(temp_workspace).resolve()

    def test_safe_path_absolute_outside_workspace(self, temp_workspace):
        """Test safe path with absolute path outside workspace."""
        sandbox = SecuritySandbox(temp_workspace)
        with pytest.raises(ValueError, match="escapes workspace"):
            sandbox.safe_path("/etc/passwd")

    def test_safe_path_with_traversal(self, temp_workspace):
        """Test safe path with path traversal attempt."""
        sandbox = SecuritySandbox(temp_workspace)
        with pytest.raises(ValueError, match="escapes workspace"):
            sandbox.safe_path("../../../etc/passwd")

    def test_safe_path_nested(self, temp_workspace):
        """Test safe path with nested directory."""
        sandbox = SecuritySandbox(temp_workspace)
        safe = sandbox.safe_path("subdir/test.txt")
        # Resolve to handle macOS symlinks
        workspace_resolved = Path(temp_workspace).resolve()
        assert safe.is_relative_to(workspace_resolved)
        assert safe.name == "test.txt"

    def test_check_write_permission_workspace(self, temp_workspace):
        """Test write permission check for workspace itself."""
        sandbox = SecuritySandbox(temp_workspace)
        assert not sandbox.check_write_permission(".")

    def test_check_write_permission_file(self, temp_workspace):
        """Test write permission check for file."""
        sandbox = SecuritySandbox(temp_workspace)
        assert sandbox.check_write_permission("test.txt")

    def test_normalize_path(self, temp_workspace):
        """Test path normalization."""
        sandbox = SecuritySandbox(temp_workspace)
        normalized = sandbox.normalize_path("subdir/test.txt")
        assert "subdir/test.txt" in normalized

    def test_normalize_path_traversal(self, temp_workspace):
        """Test normalize path with traversal returns original."""
        sandbox = SecuritySandbox(temp_workspace)
        # Should return as-is since it's unsafe
        normalized = sandbox.normalize_path("../../../etc/passwd")
        # Returns original path for error messages
        assert "../../../etc/passwd" in normalized
