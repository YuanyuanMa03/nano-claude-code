"""Tests for file_tools module."""

import pytest
import tempfile
import shutil
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from file_tools import FileTools, create_file_tools


class TestFileTools:
    """Test cases for FileTools."""

    @pytest.fixture
    def temp_workspace(self):
        """Create a temporary workspace directory."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def file_tools(self, temp_workspace):
        """Create FileTools instance with temp workspace."""
        return FileTools(temp_workspace)

    def test_read_file_success(self, file_tools, temp_workspace):
        """Test reading an existing file."""
        # Create test file
        test_file = os.path.join(temp_workspace, "test.txt")
        with open(test_file, 'w') as f:
            f.write("Hello, World!")

        result = file_tools.read_file("test.txt")
        assert "Hello, World!" in result

    def test_read_file_not_found(self, file_tools):
        """Test reading a non-existent file."""
        result = file_tools.read_file("nonexistent.txt")
        assert "Error: File not found" in result

    def test_read_file_with_limit(self, file_tools, temp_workspace):
        """Test reading file with line limit."""
        # Create test file with multiple lines
        test_file = os.path.join(temp_workspace, "test.txt")
        with open(test_file, 'w') as f:
            for i in range(10):
                f.write(f"Line {i}\n")

        result = file_tools.read_file("test.txt", limit=3)
        lines = result.split('\n')
        # Should have 3 lines plus maybe empty string at end
        assert len([l for l in lines if l.strip()]) <= 3

    def test_write_file_success(self, file_tools, temp_workspace):
        """Test writing a file."""
        result = file_tools.write_file("new.txt", "Test content")
        assert "Successfully wrote" in result
        assert "new.txt" in result

        # Verify file was created
        test_file = os.path.join(temp_workspace, "new.txt")
        assert os.path.exists(test_file)
        with open(test_file, 'r') as f:
            assert f.read() == "Test content"

    def test_write_file_creates_directories(self, file_tools, temp_workspace):
        """Test writing file creates parent directories."""
        result = file_tools.write_file("subdir/nested/file.txt", "content")
        assert "Successfully wrote" in result

        # Verify directory was created
        test_dir = os.path.join(temp_workspace, "subdir/nested")
        assert os.path.exists(test_dir)

    def test_edit_file_success(self, file_tools, temp_workspace):
        """Test editing a file."""
        # Create test file
        test_file = os.path.join(temp_workspace, "test.txt")
        with open(test_file, 'w') as f:
            f.write("Hello World\nGoodbye World")

        result = file_tools.edit_file("test.txt", "Hello", "Hi")
        assert "Successfully replaced" in result

        # Verify edit
        with open(test_file, 'r') as f:
            content = f.read()
        assert "Hi World" in content

    def test_edit_file_old_text_not_found(self, file_tools, temp_workspace):
        """Test editing file when old text is not found."""
        # Create test file
        test_file = os.path.join(temp_workspace, "test.txt")
        with open(test_file, 'w') as f:
            f.write("Hello World")

        result = file_tools.edit_file("test.txt", "Goodbye", "Hi")
        assert "not found" in result

    def test_edit_file_not_found(self, file_tools):
        """Test editing non-existent file."""
        result = file_tools.edit_file("nonexistent.txt", "old", "new")
        assert "Error: File not found" in result

    def test_read_file_path_traversal(self, file_tools, temp_workspace):
        """Test reading file with path traversal attempt."""
        result = file_tools.read_file("../../../etc/passwd")
        assert "Error:" in result

    def test_write_file_path_traversal(self, file_tools):
        """Test writing file with path traversal attempt."""
        result = file_tools.write_file("../../../etc/passwd", "malicious")
        assert "Error:" in result

    def test_create_file_tools(self, temp_workspace):
        """Test create_file_tools helper function."""
        tools = create_file_tools(temp_workspace)
        assert "read_file" in tools
        assert "write_file" in tools
        assert "edit_file" in tools

        # Test that handlers are callable
        assert callable(tools["read_file"])
        assert callable(tools["write_file"])
        assert callable(tools["edit_file"])
