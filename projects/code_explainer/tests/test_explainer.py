"""Tests for code explainer"""
import pytest
from unittest.mock import Mock, patch
from app import CodeExplainer


@patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'})
def test_explainer_init():
    """Test CodeExplainer initialization."""
    explainer = CodeExplainer()
    assert explainer.client is not None


@patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'})
def test_explain():
    """Test code explanation."""
    explainer = CodeExplainer()
    with patch.object(explainer.client.chat.completions, 'create') as mock_create:
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "This code prints hello"
        mock_create.return_value = mock_response
        
        result = explainer.explain("print('hello')")
        assert "hello" in result.lower()

