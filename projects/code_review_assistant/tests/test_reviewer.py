"""Tests for code review assistant"""
import pytest
from unittest.mock import Mock, patch
from app import CodeReviewAssistant


@patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'})
def test_reviewer_init():
    """Test CodeReviewAssistant initialization."""
    reviewer = CodeReviewAssistant()
    assert reviewer.client is not None


@patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'})
def test_review():
    """Test code review."""
    reviewer = CodeReviewAssistant()
    with patch.object(reviewer.client.chat.completions, 'create') as mock_create:
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Review: Good code"
        mock_create.return_value = mock_response
        
        result = reviewer.review("def test(): pass")
        assert len(result) > 0

