#!/usr/bin/env python3
"""Test script for text rendering functionality."""

import sys
import cv2
from whiteboard_animator import render_text_to_image

def test_basic_text():
    """Test basic text rendering."""
    print("Testing basic text rendering...")
    
    text_config = {
        "text": "Hello World!",
        "font": "DejaVuSans",
        "size": 48,
        "color": (0, 0, 255),  # Red in RGB
        "style": "normal",
        "align": "center"
    }
    
    img = render_text_to_image(text_config, 800, 600)
    
    if img is not None and img.shape == (600, 800, 3):
        print("✓ Basic text rendering successful")
        cv2.imwrite("/tmp/test_basic_text.png", img)
        return True
    else:
        print("✗ Basic text rendering failed")
        return False

def test_multiline_text():
    """Test multi-line text rendering."""
    print("Testing multi-line text rendering...")
    
    text_config = {
        "text": "Line 1\nLine 2\nLine 3",
        "font": "DejaVuSans",
        "size": 36,
        "color": (0, 128, 0),
        "style": "normal",
        "line_height": 1.5,
        "align": "left"
    }
    
    img = render_text_to_image(text_config, 800, 600)
    
    if img is not None:
        print("✓ Multi-line text rendering successful")
        cv2.imwrite("/tmp/test_multiline_text.png", img)
        return True
    else:
        print("✗ Multi-line text rendering failed")
        return False

def test_styled_text():
    """Test text with styles."""
    print("Testing styled text rendering...")
    
    text_config = {
        "text": "Bold Text Test",
        "font": "DejaVuSans",
        "size": 52,
        "color": (128, 0, 128),
        "style": "bold",
        "align": "center"
    }
    
    img = render_text_to_image(text_config, 800, 600)
    
    if img is not None:
        print("✓ Styled text rendering successful")
        cv2.imwrite("/tmp/test_styled_text.png", img)
        return True
    else:
        print("✗ Styled text rendering failed")
        return False

def test_hex_color():
    """Test text with hex color."""
    print("Testing hex color...")
    
    text_config = {
        "text": "Hex Color Test",
        "font": "DejaVuSans",
        "size": 42,
        "color": "#FF5500",
        "align": "center"
    }
    
    img = render_text_to_image(text_config, 800, 600)
    
    if img is not None:
        print("✓ Hex color rendering successful")
        cv2.imwrite("/tmp/test_hex_color.png", img)
        return True
    else:
        print("✗ Hex color rendering failed")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Text Rendering Tests")
    print("=" * 60)
    
    tests = [
        test_basic_text,
        test_multiline_text,
        test_styled_text,
        test_hex_color
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
            results.append(False)
        print()
    
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} tests passed")
    print("=" * 60)
    
    sys.exit(0 if all(results) else 1)
