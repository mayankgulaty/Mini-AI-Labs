"""Tests for text to speech converter"""
import pytest
from unittest.mock import Mock, patch
from app import TextToSpeech


@patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'})
def test_tts_init():
    """Test TextToSpeech initialization."""
    tts = TextToSpeech()
    assert tts.client is not None
    assert len(tts.available_voices) > 0


@patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'})
def test_convert():
    """Test text conversion."""
    tts = TextToSpeech()
    with patch.object(tts.client.audio.speech, 'create') as mock_create:
        mock_response = Mock()
        mock_response.stream_to_file = Mock()
        mock_create.return_value = mock_response
        
        result = tts.convert("Test text", "alloy", "test.mp3")
        assert result == "test.mp3"

