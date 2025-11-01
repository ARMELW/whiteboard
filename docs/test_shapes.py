#!/usr/bin/env python3
"""Test script for geometric shapes feature."""

import sys
import cv2
import numpy as np
from whiteboard_animator import render_shape_to_image

def test_circle():
    """Test circle rendering."""
    print("Testing circle rendering...")
    
    shape_config = {
        "shape": "circle",
        "color": (0, 0, 255),  # Red in BGR
        "fill_color": (200, 200, 255),  # Light red fill
        "stroke_width": 3,
        "position": {"x": 400, "y": 300},
        "size": 100
    }
    
    img = render_shape_to_image(shape_config, 800, 600)
    
    if img is not None and img.shape == (600, 800, 3):
        print("✓ Circle rendering successful")
        cv2.imwrite("/tmp/test_circle.png", img)
        return True
    else:
        print("✗ Circle rendering failed")
        return False

def test_rectangle():
    """Test rectangle rendering."""
    print("Testing rectangle rendering...")
    
    shape_config = {
        "shape": "rectangle",
        "color": (255, 0, 0),  # Blue in BGR
        "fill_color": (255, 200, 200),  # Light blue fill
        "stroke_width": 3,
        "position": {"x": 400, "y": 300},
        "width": 200,
        "height": 150
    }
    
    img = render_shape_to_image(shape_config, 800, 600)
    
    if img is not None and img.shape == (600, 800, 3):
        print("✓ Rectangle rendering successful")
        cv2.imwrite("/tmp/test_rectangle.png", img)
        return True
    else:
        print("✗ Rectangle rendering failed")
        return False

def test_triangle():
    """Test triangle rendering."""
    print("Testing triangle rendering...")
    
    shape_config = {
        "shape": "triangle",
        "color": (0, 255, 0),  # Green in BGR
        "fill_color": (200, 255, 200),  # Light green fill
        "stroke_width": 3,
        "position": {"x": 400, "y": 300},
        "size": 150
    }
    
    img = render_shape_to_image(shape_config, 800, 600)
    
    if img is not None and img.shape == (600, 800, 3):
        print("✓ Triangle rendering successful")
        cv2.imwrite("/tmp/test_triangle.png", img)
        return True
    else:
        print("✗ Triangle rendering failed")
        return False

def test_arrow():
    """Test arrow rendering."""
    print("Testing arrow rendering...")
    
    shape_config = {
        "shape": "arrow",
        "color": (0, 0, 0),  # Black in BGR
        "fill_color": (100, 100, 100),  # Gray fill for arrow head
        "stroke_width": 3,
        "start": [100, 300],
        "end": [700, 300],
        "arrow_size": 30
    }
    
    img = render_shape_to_image(shape_config, 800, 600)
    
    if img is not None and img.shape == (600, 800, 3):
        print("✓ Arrow rendering successful")
        cv2.imwrite("/tmp/test_arrow.png", img)
        return True
    else:
        print("✗ Arrow rendering failed")
        return False

def test_polygon():
    """Test polygon rendering."""
    print("Testing polygon rendering...")
    
    shape_config = {
        "shape": "polygon",
        "color": (128, 0, 128),  # Purple in BGR
        "fill_color": (200, 150, 200),  # Light purple fill
        "stroke_width": 3,
        "points": [
            [400, 150],
            [500, 250],
            [450, 400],
            [350, 400],
            [300, 250]
        ]
    }
    
    img = render_shape_to_image(shape_config, 800, 600)
    
    if img is not None and img.shape == (600, 800, 3):
        print("✓ Polygon rendering successful")
        cv2.imwrite("/tmp/test_polygon.png", img)
        return True
    else:
        print("✗ Polygon rendering failed")
        return False

def test_line():
    """Test line rendering."""
    print("Testing line rendering...")
    
    shape_config = {
        "shape": "line",
        "color": (255, 128, 0),  # Orange in BGR
        "stroke_width": 4,
        "start": [100, 100],
        "end": [700, 500]
    }
    
    img = render_shape_to_image(shape_config, 800, 600)
    
    if img is not None and img.shape == (600, 800, 3):
        print("✓ Line rendering successful")
        cv2.imwrite("/tmp/test_line.png", img)
        return True
    else:
        print("✗ Line rendering failed")
        return False

def test_hex_colors():
    """Test hex color support."""
    print("Testing hex color support...")
    
    shape_config = {
        "shape": "circle",
        "color": "#FF0000",  # Red in hex
        "fill_color": "#FFCCCC",  # Light red in hex
        "stroke_width": 3,
        "position": {"x": 400, "y": 300},
        "size": 80
    }
    
    img = render_shape_to_image(shape_config, 800, 600)
    
    if img is not None and img.shape == (600, 800, 3):
        print("✓ Hex color support successful")
        cv2.imwrite("/tmp/test_hex_colors.png", img)
        return True
    else:
        print("✗ Hex color support failed")
        return False

if __name__ == "__main__":
    print("\n=== Testing Geometric Shapes Feature ===\n")
    
    tests = [
        test_circle,
        test_rectangle,
        test_triangle,
        test_arrow,
        test_polygon,
        test_line,
        test_hex_colors
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        if test():
            passed += 1
        else:
            failed += 1
        print()
    
    print(f"=== Test Results ===")
    print(f"Passed: {passed}/{len(tests)}")
    print(f"Failed: {failed}/{len(tests)}")
    
    if failed == 0:
        print("\n✓ All tests passed!")
        sys.exit(0)
    else:
        print(f"\n✗ {failed} test(s) failed")
        sys.exit(1)
