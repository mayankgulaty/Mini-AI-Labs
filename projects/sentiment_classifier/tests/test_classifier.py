"""
Tests for sentiment classifier
"""

import pytest
from unittest.mock import Mock, patch
from app import SentimentClassifier


@patch('app.AutoTokenizer')
@patch('app.AutoModelForSequenceClassification')
def test_sentiment_classifier_init(mock_model_class, mock_tokenizer_class):
    """Test SentimentClassifier initialization."""
    mock_tokenizer = Mock()
    mock_model = Mock()
    mock_tokenizer_class.from_pretrained.return_value = mock_tokenizer
    mock_model_class.from_pretrained.return_value = mock_model
    
    classifier = SentimentClassifier()
    assert classifier.tokenizer == mock_tokenizer
    assert classifier.model == mock_model
    assert classifier.label_map[0] == "NEGATIVE"
    assert classifier.label_map[1] == "NEUTRAL"
    assert classifier.label_map[2] == "POSITIVE"


@patch('app.AutoTokenizer')
@patch('app.AutoModelForSequenceClassification')
def test_classify(mock_model_class, mock_tokenizer_class):
    """Test sentiment classification."""
    mock_tokenizer = Mock()
    mock_model = Mock()
    mock_tokenizer_class.from_pretrained.return_value = mock_tokenizer
    mock_model_class.from_pretrained.return_value = mock_model
    
    # Mock tokenizer output
    mock_tokenizer.return_value = {'input_ids': Mock(), 'attention_mask': Mock()}
    
    classifier = SentimentClassifier()
    # Note: Full test would require mocking torch operations
    # This is a basic structure test

