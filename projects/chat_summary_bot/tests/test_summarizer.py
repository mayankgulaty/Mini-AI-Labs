"""
Tests for chat summary bot
"""

import pytest
import os
from unittest.mock import Mock, patch
from app import summarize_chat, read_chat_file


def test_read_chat_file(tmp_path):
    """Test reading chat file."""
    test_file = tmp_path / "test_chat.txt"
    test_file.write_text("Hello\nWorld\nTest")
    
    content = read_chat_file(str(test_file))
    assert content == "Hello\nWorld\nTest"


@patch('app.client')
def test_summarize_chat(mock_client):
    """Test chat summarization."""
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = "This is a test summary"
    mock_client.chat.completions.create.return_value = mock_response
    
    summary = summarize_chat("Test chat content")
    assert summary == "This is a test summary"
    assert mock_client.chat.completions.create.called

