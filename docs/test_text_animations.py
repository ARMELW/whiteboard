#!/usr/bin/env python3
"""Test script for advanced text animation features."""

import sys
import cv2
import numpy as np
from whiteboard_animator import render_text_to_image

def test_rtl_text():
    """Test Right-to-Left (RTL) text rendering."""
    print("Testing RTL text rendering (Arabic)...")
    
    text_config = {
        "text": "مرحبا بالعالم",  # "Hello World" in Arabic
        "font": "DejaVuSans",
        "size": 48,
        "color": (0, 0, 255),
        "direction": "rtl",
        "align": "right"
    }
    
    img = render_text_to_image(text_config, 800, 600)
    
    if img is not None and img.shape == (600, 800, 3):
        print("✓ RTL text rendering successful")
        cv2.imwrite("/tmp/test_rtl_text.png", img)
        return True
    else:
        print("✗ RTL text rendering failed")
        return False

def test_text_with_shadow():
    """Test text with shadow effect."""
    print("Testing text with shadow effect...")
    
    text_config = {
        "text": "Shadow Text",
        "font": "DejaVuSans",
        "size": 56,
        "color": "#0066CC",
        "align": "center",
        "text_effects": {
            "shadow": {
                "offset": (3, 3),
                "color": "#888888"
            }
        }
    }
    
    img = render_text_to_image(text_config, 800, 600)
    
    if img is not None:
        print("✓ Text with shadow rendering successful")
        cv2.imwrite("/tmp/test_text_shadow.png", img)
        return True
    else:
        print("✗ Text with shadow rendering failed")
        return False

def test_text_with_outline():
    """Test text with outline effect."""
    print("Testing text with outline effect...")
    
    text_config = {
        "text": "Outlined Text",
        "font": "DejaVuSans",
        "size": 64,
        "color": "#FFFF00",
        "style": "bold",
        "align": "center",
        "text_effects": {
            "outline": {
                "width": 2,
                "color": "#000000"
            }
        }
    }
    
    img = render_text_to_image(text_config, 800, 600)
    
    if img is not None:
        print("✓ Text with outline rendering successful")
        cv2.imwrite("/tmp/test_text_outline.png", img)
        return True
    else:
        print("✗ Text with outline rendering failed")
        return False

def test_vertical_text():
    """Test vertical text rendering."""
    print("Testing vertical text rendering...")
    
    text_config = {
        "text": "縦書き",  # "Vertical writing" in Japanese
        "font": "DejaVuSans",
        "size": 48,
        "color": (0, 0, 0),
        "vertical": True,
        "align": "center"
    }
    
    img = render_text_to_image(text_config, 800, 600)
    
    if img is not None:
        print("✓ Vertical text rendering successful")
        cv2.imwrite("/tmp/test_vertical_text.png", img)
        return True
    else:
        print("✗ Vertical text rendering failed")
        return False

def test_font_fallback():
    """Test font fallback chain."""
    print("Testing font fallback chain...")
    
    text_config = {
        "text": "Hello 你好 مرحبا",  # Mixed scripts
        "font": "NonExistentFont",
        "size": 42,
        "color": "#333333",
        "align": "center",
        "font_fallbacks": ["DejaVuSans", "NotoSans", "Arial"]
    }
    
    img = render_text_to_image(text_config, 800, 600)
    
    if img is not None:
        print("✓ Font fallback rendering successful")
        cv2.imwrite("/tmp/test_font_fallback.png", img)
        return True
    else:
        print("✗ Font fallback rendering failed")
        return False

def test_combined_effects():
    """Test text with multiple combined effects."""
    print("Testing combined text effects...")
    
    text_config = {
        "text": "Amazing Text!",
        "font": "DejaVuSans",
        "size": 72,
        "color": "#FF0066",
        "style": "bold",
        "align": "center",
        "text_effects": {
            "shadow": {
                "offset": (4, 4),
                "color": "#000000"
            },
            "outline": {
                "width": 1,
                "color": "#FFFFFF"
            }
        }
    }
    
    img = render_text_to_image(text_config, 800, 600)
    
    if img is not None:
        print("✓ Combined effects rendering successful")
        cv2.imwrite("/tmp/test_combined_effects.png", img)
        return True
    else:
        print("✗ Combined effects rendering failed")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Advanced Text Animation and Multilingual Tests")
    print("=" * 60)
    
    tests = [
        test_rtl_text,
        test_text_with_shadow,
        test_text_with_outline,
        test_vertical_text,
        test_font_fallback,
        test_combined_effects
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
            import traceback
            traceback.print_exc()
            results.append(False)
        print()
    
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} tests passed")
    print("=" * 60)
    
    sys.exit(0 if all(results) else 1)
