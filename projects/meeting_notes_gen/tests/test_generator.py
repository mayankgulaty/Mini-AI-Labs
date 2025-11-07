"""Tests for meeting notes generator"""
import pytest
from unittest.mock import Mock, patch
from app import MeetingNotesGenerator


@patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'})
def test_generator_init():
    """Test MeetingNotesGenerator initialization."""
    generator = MeetingNotesGenerator()
    assert generator.client is not None


@patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'})
def test_generate():
    """Test notes generation."""
    generator = MeetingNotesGenerator()
    with patch.object(generator.client.chat.completions, 'create') as mock_create:
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Meeting Summary: Test"
        mock_create.return_value = mock_response
        
        result = generator.generate("Test transcript")
        assert len(result) > 0

