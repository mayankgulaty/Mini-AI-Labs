"""
Tests for image captioner
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from PIL import Image
import io
from app import ImageCaptioner


def create_test_image():
    """Create a test image."""
    img = Image.new('RGB', (100, 100), color='red')
    return img


@patch('app.BlipProcessor')
@patch('app.BlipForConditionalGeneration')
def test_image_captioner_init(mock_model_class, mock_processor_class):
    """Test ImageCaptioner initialization."""
    mock_processor = Mock()
    mock_model = Mock()
    mock_processor_class.from_pretrained.return_value = mock_processor
    mock_model_class.from_pretrained.return_value = mock_model
    
    captioner = ImageCaptioner()
    assert captioner.processor == mock_processor
    assert captioner.model == mock_model

