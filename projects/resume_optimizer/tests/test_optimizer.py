"""
Tests for resume optimizer
"""

import pytest
import os
from unittest.mock import Mock, patch, mock_open
from app import ResumeOptimizer


def test_resume_optimizer_init():
    """Test ResumeOptimizer initialization."""
    with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
        optimizer = ResumeOptimizer()
        assert optimizer.llm is not None
        assert optimizer.chain is not None


def test_resume_optimizer_init_missing_key():
    """Test that missing API key raises error."""
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError, match="OPENAI_API_KEY not set"):
            ResumeOptimizer()


@patch('app.extract_text')
def test_extract_text_from_pdf(mock_extract):
    """Test PDF text extraction."""
    mock_extract.return_value = "Sample resume text"
    
    with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
        optimizer = ResumeOptimizer()
        text = optimizer.extract_text_from_pdf("test.pdf")
        assert text == "Sample resume text"


@patch('app.extract_text')
def test_extract_text_from_pdf_empty(mock_extract):
    """Test PDF extraction with empty content."""
    mock_extract.return_value = "   "
    
    with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
        optimizer = ResumeOptimizer()
        with pytest.raises(ValueError, match="No text could be extracted"):
            optimizer.extract_text_from_pdf("test.pdf")

