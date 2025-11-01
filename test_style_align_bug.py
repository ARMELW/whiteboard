#!/usr/bin/env python3
"""Test to reproduce the bug where text style and alignment are not applied."""

import sys
import os
import json
import cv2
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))

from whiteboard_animator import compose_layers, render_text_to_image

def test_text_style_normal():
    """Test normal style text."""
    print("\n1. Testing normal style text...")
    
    text_config = {
        'text': 'Normal Text',
        'font': 'Pacifico',
        'size': 37,
        'color': [0, 0, 0],
        'style': 'normal',
        'align': 'center'
    }
    
    result = render_text_to_image(text_config, 800, 450)
    
    if result is not None:
        print("   ✓ Normal style text rendered")
        return True
    else:
        print("   ✗ Normal style text failed to render")
        return False

def test_text_style_bold():
    """Test bold style text."""
    print("\n2. Testing bold style text...")
    
    text_config = {
        'text': 'Bold Text',
        'font': 'Pacifico',
        'size': 37,
        'color': [0, 0, 0],
        'style': 'bold',
        'align': 'center'
    }
    
    result = render_text_to_image(text_config, 800, 450)
    
    if result is not None:
        print("   ✓ Bold style text rendered")
        return True
    else:
        print("   ✗ Bold style text failed to render")
        return False

def test_text_style_italic():
    """Test italic style text."""
    print("\n3. Testing italic style text...")
    
    text_config = {
        'text': 'Italic Text',
        'font': 'Pacifico',
        'size': 37,
        'color': [0, 0, 0],
        'style': 'italic',
        'align': 'center'
    }
    
    result = render_text_to_image(text_config, 800, 450)
    
    if result is not None:
        print("   ✓ Italic style text rendered")
        return True
    else:
        print("   ✗ Italic style text failed to render")
        return False

def test_text_style_bold_italic():
    """Test bold italic style text."""
    print("\n4. Testing bold italic style text...")
    
    text_config = {
        'text': 'Bold Italic Text',
        'font': 'Pacifico',
        'size': 37,
        'color': [0, 0, 0],
        'style': 'bold italic',
        'align': 'center'
    }
    
    result = render_text_to_image(text_config, 800, 450)
    
    if result is not None:
        print("   ✓ Bold italic style text rendered")
        return True
    else:
        print("   ✗ Bold italic style text failed to render")
        return False

def test_text_align_left():
    """Test left alignment."""
    print("\n5. Testing left alignment...")
    
    text_config = {
        'text': 'Left Aligned',
        'font': 'DejaVuSans',
        'size': 37,
        'color': [0, 0, 0],
        'style': 'normal',
        'align': 'left'
    }
    
    result = render_text_to_image(text_config, 800, 450)
    
    if result is not None:
        print("   ✓ Left aligned text rendered")
        return True
    else:
        print("   ✗ Left aligned text failed to render")
        return False

def test_text_align_center():
    """Test center alignment."""
    print("\n6. Testing center alignment...")
    
    text_config = {
        'text': 'Center Aligned',
        'font': 'DejaVuSans',
        'size': 37,
        'color': [0, 0, 0],
        'style': 'normal',
        'align': 'center'
    }
    
    result = render_text_to_image(text_config, 800, 450)
    
    if result is not None:
        print("   ✓ Center aligned text rendered")
        return True
    else:
        print("   ✗ Center aligned text failed to render")
        return False

def test_text_align_right():
    """Test right alignment."""
    print("\n7. Testing right alignment...")
    
    text_config = {
        'text': 'Right Aligned',
        'font': 'DejaVuSans',
        'size': 37,
        'color': [0, 0, 0],
        'style': 'normal',
        'align': 'right'
    }
    
    result = render_text_to_image(text_config, 800, 450)
    
    if result is not None:
        print("   ✓ Right aligned text rendered")
        return True
    else:
        print("   ✗ Right aligned text failed to render")
        return False

def test_full_example():
    """Test the full example from the issue."""
    print("\n8. Testing full example from issue...")
    
    config = {
        "slides": [
            {
                "index": 0,
                "duration": 2,
                "skip_rate": 10,
                "layers": [
                    {
                        "type": "text",
                        "z_index": 0,
                        "mode": "draw",
                        "width": 799.2,
                        "height": 106.56,
                        "scale": 1,
                        "source_width": 800,
                        "source_height": 450,
                        "opacity": 1,
                        "skip_rate": 12,
                        "anchor_point": "center",
                        "position": {
                            "x": 163,
                            "y": 129
                        },
                        "text_config": {
                            "text": "Votre texte ici",
                            "font_path": "fonts/Pacifico.ttf",
                            "font": "Pacifico",
                            "size": 37,
                            "style": "normal",
                            "color": [0, 0, 0],
                            "align": "center"
                        }
                    }
                ]
            }
        ]
    }
    
    layers_config = config['slides'][0]['layers']
    
    try:
        result = compose_layers(layers_config, 800, 450)
        if result is not None:
            print("   ✓ Full example rendered successfully")
            return True
        else:
            print("   ✗ Full example failed to render")
            return False
    except Exception as e:
        print(f"   ✗ Full example raised exception: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 70)
    print("Testing Text Style and Alignment Bug")
    print("=" * 70)
    
    tests = [
        test_text_style_normal,
        test_text_style_bold,
        test_text_style_italic,
        test_text_style_bold_italic,
        test_text_align_left,
        test_text_align_center,
        test_text_align_right,
        test_full_example
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"   ✗ Test crashed: {e}")
            import traceback
            traceback.print_exc()
            results.append(False)
    
    print("\n" + "=" * 70)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} tests passed")
    print("=" * 70)
    
    sys.exit(0 if all(results) else 1)
