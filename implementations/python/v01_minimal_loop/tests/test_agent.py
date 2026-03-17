"""Tests for agent module."""

import pytest
from unittest.mock import patch, MagicMock
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from agent import AgentLoop


class TestAgentLoop:
    """Test cases for AgentLoop."""

    @pytest.fixture
    def mock_anthropic_client(self):
        """Create a mock Anthropic client."""
        with patch('agent.Anthropic') as mock:
            yield mock

    @pytest.fixture
    def agent(self, mock_anthropic_client):
        """Create an agent instance with mocked client."""
        # Mock the client creation
        mock_client_instance = MagicMock()
        mock_anthropic_client.return_value = mock_client_instance

        agent = AgentLoop(api_key="test-key", model="test-model")
        agent.client = mock_client_instance
        return agent

    def test_agent_initialization(self, mock_anthropic_client):
        """Test agent initialization."""
        agent = AgentLoop(api_key="test-key", model="test-model")
        assert agent.model == "test-model"
        assert len(agent.tools) == 1
        assert agent.tools[0]["name"] == "bash"

    def test_extract_text_from_response(self, agent):
        """Test text extraction from response blocks."""
        # Create mock content blocks
        mock_content = [
            MagicMock(type="text", text="First line"),
            MagicMock(type="text", text="Second line"),
        ]
        result = agent._extract_text(mock_content)
        assert result == "First line\nSecond line"

    def test_execute_bash_tool(self, agent):
        """Test executing the bash tool."""
        with patch('agent.run_bash') as mock_bash:
            mock_bash.return_value = "Command output"
            result = agent._execute_tool("bash", {"command": "echo test"})
            assert result == "Command output"
            mock_bash.assert_called_once_with("echo test", 120)

    def test_execute_unknown_tool(self, agent):
        """Test executing an unknown tool."""
        result = agent._execute_tool("unknown_tool", {})
        assert "Error" in result
        assert "Unknown tool" in result

    def test_agent_loop_with_text_only_response(self, agent):
        """Test agent loop when LLM responds with text only."""
        # Mock the LLM response with text only
        mock_response = MagicMock()
        mock_response.stop_reason = "end_turn"
        mock_response.content = [
            MagicMock(type="text", text="Final answer")
        ]
        agent.client.messages.create.return_value = mock_response

        result = agent.run("Test query")
        assert result == "Final answer"

    def test_agent_loop_with_tool_use(self, agent):
        """Test agent loop with tool use."""
        # First call: LLM wants to use tool
        first_response = MagicMock()
        first_response.stop_reason = "tool_use"
        first_response.content = [
            MagicMock(
                type="tool_use",
                id="tool_123",
                name="bash",
                input={"command": "ls"}
            )
        ]

        # Second call: LLM responds with final answer
        second_response = MagicMock()
        second_response.stop_reason = "end_turn"
        second_response.content = [
            MagicMock(type="text", text="I found file.txt")
        ]

        agent.client.messages.create.side_effect = [first_response, second_response]

        # Patch _execute_tool to avoid actual bash execution
        with patch.object(agent, '_execute_tool', return_value="file.txt") as mock_exec:
            result = agent.run("List files")
            assert result == "I found file.txt"
            # Verify that _execute_tool was called
            assert mock_exec.call_count == 1
