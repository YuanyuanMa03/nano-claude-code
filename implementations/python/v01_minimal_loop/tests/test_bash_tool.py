"""Tests for bash_tool module."""

import pytest
from unittest.mock import patch, MagicMock
import subprocess

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from bash_tool import run_bash


class TestBashTool:
    """Test cases for bash tool."""

    def test_run_simple_command(self):
        """Test running a simple command."""
        result = run_bash("echo 'Hello, World!'")
        assert "Hello, World!" in result

    def test_run_command_with_error(self):
        """Test running a command that produces an error."""
        result = run_bash("ls /nonexistent_directory_12345")
        assert "Error" in result or "cannot access" in result.lower() or "No such file" in result

    @patch('subprocess.run')
    def test_command_timeout(self, mock_run):
        """Test command timeout handling."""
        mock_run.side_effect = subprocess.TimeoutExpired(cmd=["sleep"], timeout=5)
        result = run_bash("sleep 10", timeout=5)
        assert "timed out" in result.lower()

    def test_working_directory(self):
        """Test that commands run in the current directory."""
        result = run_bash("pwd")
        assert os.path.exists(result.strip().split('\n')[-1])

    def test_command_with_output(self):
        """Test command that produces output."""
        result = run_bash("python --version")
        assert result.strip() != ""
