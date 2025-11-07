"""Tests for PDF Q&A bot"""
import pytest
from unittest.mock import Mock, patch
from app import PDFQABot


@patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'})
def test_bot_init():
    """Test PDFQABot initialization."""
    bot = PDFQABot()
    assert bot.client is not None


@patch('app.extract_text')
@patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'})
def test_answer_question(mock_extract):
    """Test question answering."""
    mock_extract.return_value = "Test document content"
    bot = PDFQABot()
    with patch.object(bot.client.chat.completions, 'create') as mock_create:
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Test answer"
        mock_create.return_value = mock_response
        
        result = bot.answer_question("test content", "test question")
        assert len(result) > 0

