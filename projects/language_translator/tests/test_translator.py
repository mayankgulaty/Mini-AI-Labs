"""Tests for language translator"""
import pytest
from unittest.mock import Mock, patch
from app import LanguageTranslator


@patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'})
def test_translator_init():
    """Test LanguageTranslator initialization."""
    translator = LanguageTranslator()
    assert translator.client is not None


@patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'})
def test_translate():
    """Test translation."""
    translator = LanguageTranslator()
    with patch.object(translator.client.chat.completions, 'create') as mock_create:
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Hola"
        mock_create.return_value = mock_response
        
        result = translator.translate("Hello", "en", "es")
        assert result == "Hola"

