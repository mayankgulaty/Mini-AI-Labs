"""Tests for recipe generator"""
import pytest
from unittest.mock import Mock, patch
from app import RecipeGenerator


@patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'})
def test_generator_init():
    """Test RecipeGenerator initialization."""
    generator = RecipeGenerator()
    assert generator.client is not None


@patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'})
def test_generate():
    """Test recipe generation."""
    generator = RecipeGenerator()
    with patch.object(generator.client.chat.completions, 'create') as mock_create:
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Recipe: Test Recipe"
        mock_create.return_value = mock_response
        
        result = generator.generate("chicken, tomatoes")
        assert len(result) > 0

