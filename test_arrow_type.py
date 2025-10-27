#!/usr/bin/env python3
"""Test script for arrow type layer feature."""

import sys
import cv2
import numpy as np
from whiteboard_animator import draw_arrow_progressive

def test_arrow_progressive_drawing():
    """Test progressive arrow drawing at different progress levels."""
    print("Testing progressive arrow drawing...")
    
    arrow_config = {
        "start": [100, 300],
        "end": [700, 300],
        "color": (0, 0, 0),  # Black in BGR
        "fill_color": (100, 100, 100),  # Gray fill
        "stroke_width": 3,
        "arrow_size": 30
    }
    
    # Test at different progress levels
    progress_levels = [0.0, 0.25, 0.5, 0.75, 0.85, 0.95, 1.0]
    
    for progress in progress_levels:
        canvas = np.ones((600, 800, 3), dtype=np.uint8) * 255
        result = draw_arrow_progressive(canvas, arrow_config, progress, 800, 600)
        
        if result is not None and result.shape == (600, 800, 3):
            filename = f"/tmp/test_arrow_progress_{int(progress*100):03d}.png"
            cv2.imwrite(filename, result)
            print(f"  ✓ Progress {progress:.2f} successful -> {filename}")
        else:
            print(f"  ✗ Progress {progress:.2f} failed")
            return False
    
    print("✓ Progressive arrow drawing test successful")
    return True


def test_arrow_with_hex_color():
    """Test arrow drawing with hex color."""
    print("Testing arrow with hex color...")
    
    arrow_config = {
        "start": [100, 300],
        "end": [700, 300],
        "color": "#FF0000",  # Red
        "fill_color": "#FFAAAA",  # Light red
        "stroke_width": 4,
        "arrow_size": 40
    }
    
    canvas = np.ones((600, 800, 3), dtype=np.uint8) * 255
    result = draw_arrow_progressive(canvas, arrow_config, 1.0, 800, 600)
    
    if result is not None and result.shape == (600, 800, 3):
        cv2.imwrite("/tmp/test_arrow_hex_color.png", result)
        print("✓ Hex color arrow test successful")
        return True
    else:
        print("✗ Hex color arrow test failed")
        return False


def test_arrow_diagonal():
    """Test diagonal arrow."""
    print("Testing diagonal arrow...")
    
    arrow_config = {
        "start": [100, 500],
        "end": [700, 100],
        "color": [0, 255, 0],  # Green (RGB list)
        "fill_color": [100, 255, 100],
        "stroke_width": 3,
        "arrow_size": 35
    }
    
    canvas = np.ones((600, 800, 3), dtype=np.uint8) * 255
    result = draw_arrow_progressive(canvas, arrow_config, 1.0, 800, 600)
    
    if result is not None and result.shape == (600, 800, 3):
        cv2.imwrite("/tmp/test_arrow_diagonal.png", result)
        print("✓ Diagonal arrow test successful")
        return True
    else:
        print("✗ Diagonal arrow test failed")
        return False


def test_arrow_without_fill():
    """Test arrow without fill color."""
    print("Testing arrow without fill...")
    
    arrow_config = {
        "start": [100, 300],
        "end": [700, 300],
        "color": (255, 0, 255),  # Magenta
        "stroke_width": 3,
        "arrow_size": 30
    }
    
    canvas = np.ones((600, 800, 3), dtype=np.uint8) * 255
    result = draw_arrow_progressive(canvas, arrow_config, 1.0, 800, 600)
    
    if result is not None and result.shape == (600, 800, 3):
        cv2.imwrite("/tmp/test_arrow_no_fill.png", result)
        print("✓ No-fill arrow test successful")
        return True
    else:
        print("✗ No-fill arrow test failed")
        return False


def main():
    """Run all tests."""
    print("=== Testing Arrow Type Feature ===\n")
    
    tests = [
        test_arrow_progressive_drawing,
        test_arrow_with_hex_color,
        test_arrow_diagonal,
        test_arrow_without_fill
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
            print()
        except Exception as e:
            print(f"✗ Test failed with exception: {e}\n")
            results.append(False)
    
    passed = sum(results)
    total = len(results)
    
    print("=== Test Results ===")
    print(f"Passed: {passed}/{total}")
    print(f"Failed: {total - passed}/{total}")
    
    if passed == total:
        print("\n✓ All tests passed!")
        return 0
    else:
        print(f"\n✗ Some tests failed")
        return 1


if __name__ == '__main__':
    sys.exit(main())
