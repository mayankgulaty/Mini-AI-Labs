"""Tests for email writer"""
import pytest
from unittest.mock import Mock, patch
from app import EmailWriter


@patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'})
def test_writer_init():
    """Test EmailWriter initialization."""
    writer = EmailWriter()
    assert writer.client is not None


@patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'})
def test_write():
    """Test email generation."""
    writer = EmailWriter()
    with patch.object(writer.client.chat.completions, 'create') as mock_create:
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Subject: Test\n\nBody"
        mock_create.return_value = mock_response
        
        result = writer.write("test", "client", "professional")
        assert len(result) > 0

