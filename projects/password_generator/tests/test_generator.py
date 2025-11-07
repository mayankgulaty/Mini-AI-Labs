"""Tests for password generator"""
import pytest
from app import PasswordGenerator


def test_generator_init():
    """Test PasswordGenerator initialization."""
    generator = PasswordGenerator()
    assert generator is not None


def test_generate():
    """Test password generation."""
    generator = PasswordGenerator()
    password = generator.generate(12)
    assert len(password) == 12
    assert isinstance(password, str)


def test_analyze_strength():
    """Test password strength analysis."""
    generator = PasswordGenerator()
    strength, analysis = generator.analyze_strength("Test123!")
    assert strength in ["Weak", "Fair", "Good", "Strong"]
    assert "score" in analysis
    assert "feedback" in analysis

