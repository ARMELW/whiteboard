#!/usr/bin/env python3
"""
Test font resolution with fontconfig integration.
"""
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from whiteboard_animator import resolve_font_path, render_text_to_image
import cv2
import numpy as np

def test_font_resolution():
    """Test that fonts are correctly resolved using fontconfig."""
    print("=" * 70)
    print("FONT RESOLUTION TEST")
    print("=" * 70)
    print()
    
    # Test various fonts
    test_fonts = [
        ("Arial", "normal"),
        ("DejaVu Sans", "normal"),
        ("Liberation Sans", "normal"),
        ("Gargi", "normal"),  # This should fall back to a system font
        ("NonExistentFont", "normal"),  # This should return None
    ]
    
    for font_name, style in test_fonts:
        font_path = resolve_font_path(font_name, style)
        if font_path:
            print(f"✅ Font '{font_name}' ({style})")
            print(f"   Resolved to: {font_path}")
        else:
            print(f"⚠️  Font '{font_name}' ({style})")
            print(f"   Not found (will use fallback)")
        print()
    
    print("=" * 70)
    print()

def test_text_rendering_with_fonts():
    """Test text rendering with different fonts."""
    print("=" * 70)
    print("TEXT RENDERING TEST")
    print("=" * 70)
    print()
    
    # Test configurations matching the issue
    test_configs = [
        {
            "name": "DejaVu Sans (should work)",
            "text_config": {
                "text": "Votre texte ici\nleka wa",
                "font": "DejaVu Sans",
                "size": 55,
                "style": "normal",
                "color": [0, 0, 0],
                "align": "center"
            }
        },
        {
            "name": "Liberation Sans (should work)",
            "text_config": {
                "text": "Votre texte ici\nleka wa",
                "font": "Liberation Sans",
                "size": 55,
                "style": "normal",
                "color": [0, 0, 0],
                "align": "center"
            }
        },
        {
            "name": "Gargi (may fallback but should render)",
            "text_config": {
                "text": "Votre texte ici\nleka wa",
                "font": "Gargi",
                "size": 55,
                "style": "normal",
                "color": [0, 0, 0],
                "align": "center"
            }
        },
    ]
    
    for test in test_configs:
        print(f"📝 Testing: {test['name']}")
        try:
            img = render_text_to_image(test['text_config'], 800, 450)
            filename = f"test_font_{test['text_config']['font'].replace(' ', '_')}.png"
            cv2.imwrite(filename, img)
            print(f"   ✅ Rendered successfully: {filename}")
        except Exception as e:
            print(f"   ❌ Failed: {str(e)}")
        print()
    
    print("=" * 70)
    print()

if __name__ == '__main__':
    test_font_resolution()
    test_text_rendering_with_fonts()
    print("\n✨ All tests completed!")
