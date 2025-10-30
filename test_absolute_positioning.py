#!/usr/bin/env python3
"""
Test script to verify absolute positioning of layers.
Tests that all layer types use position as top-left corner.
"""

import json
import os
import sys
import tempfile
import shutil

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from whiteboard_animator import render_text_to_image, compose_layers
import numpy as np
import cv2

def test_text_absolute_positioning():
    """Test that text layers use position as top-left corner, not as anchor based on alignment."""
    print("=" * 60)
    print("Testing Text Absolute Positioning")
    print("=" * 60)
    
    target_width = 800
    target_height = 600
    
    # Test with different alignments - all should start at same position
    test_cases = [
        {'align': 'left', 'expected_x': 100},
        {'align': 'center', 'expected_x': 100},  # Should NOT center on position
        {'align': 'right', 'expected_x': 100},   # Should NOT right-align on position
    ]
    
    for test_case in test_cases:
        text_config = {
            'text': 'Test',
            'font': 'Arial',
            'size': 48,
            'color': [0, 0, 255],  # Red
            'align': test_case['align'],
            'position': {'x': 100, 'y': 50}
        }
        
        img = render_text_to_image(text_config, target_width, target_height)
        
        # Find the leftmost non-white pixel
        # Convert to grayscale and threshold
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 254, 255, cv2.THRESH_BINARY_INV)
        
        # Find non-zero pixels
        coords = cv2.findNonZero(binary)
        if coords is not None:
            x_coords = coords[:, 0, 0]
            min_x = int(np.min(x_coords))
            
            # Check if text starts at expected position (with small tolerance)
            tolerance = 5
            if abs(min_x - test_case['expected_x']) <= tolerance:
                print(f"✓ PASS: align='{test_case['align']}' - Text starts at x={min_x} (expected {test_case['expected_x']})")
            else:
                print(f"✗ FAIL: align='{test_case['align']}' - Text starts at x={min_x} (expected {test_case['expected_x']})")
                return False
        else:
            print(f"✗ FAIL: align='{test_case['align']}' - No text found in image")
            return False
    
    print("\n✓ All text positioning tests passed!")
    return True

def test_layer_composition():
    """Test that layer composition uses absolute positioning."""
    print("\n" + "=" * 60)
    print("Testing Layer Composition")
    print("=" * 60)
    
    # Create a temporary directory for test images
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Create a simple test image
        test_img = np.ones((100, 100, 3), dtype=np.uint8) * 128  # Gray square
        cv2.rectangle(test_img, (10, 10), (90, 90), (0, 0, 255), -1)  # Red square
        test_img_path = os.path.join(temp_dir, 'test.png')
        cv2.imwrite(test_img_path, test_img)
        
        # Test layer config
        layers_config = [
            {
                'type': 'image',
                'image_path': test_img_path,
                'position': {'x': 50, 'y': 50},
                'z_index': 1
            },
            {
                'type': 'text',
                'text_config': {
                    'text': 'Test',
                    'font': 'Arial',
                    'size': 24,
                    'color': [255, 0, 0],  # Blue
                    'align': 'center',  # Should not affect absolute position
                    'position': {'x': 50, 'y': 200}
                },
                'z_index': 2
            }
        ]
        
        canvas = compose_layers(layers_config, 400, 300, temp_dir)
        
        # Check if image layer is at correct position
        # The gray background should be at position (50, 50) - top-left of the image
        # The red square (inset 10px) should be at position (60, 60)
        pixel_at_topleft = canvas[50, 50]  # y, x order in numpy
        pixel_inside_red = canvas[60, 60]
        
        # Top-left should be gray (background of the test image)
        # Center of red rectangle should be red
        if (np.array_equal(pixel_at_topleft, [128, 128, 128]) and 
            np.array_equal(pixel_inside_red, [0, 0, 255])):
            print(f"✓ PASS: Image layer positioned at (50, 50) - gray at corner, red at (60,60)")
        else:
            print(f"✗ FAIL: Image layer not at expected position")
            print(f"  Pixel at (50, 50): {pixel_at_topleft} (expected [128, 128, 128])")
            print(f"  Pixel at (60, 60): {pixel_inside_red} (expected [0, 0, 255])")
            return False
        
        # Check if text starts near position (50, 200)
        # Extract a region around the text position
        text_region = canvas[200:220, 50:150]  # y:y+height, x:x+width
        gray = cv2.cvtColor(text_region, cv2.COLOR_BGR2GRAY)
        has_text = np.any(gray < 250)
        
        if has_text:
            print(f"✓ PASS: Text layer positioned near (50, 200)")
        else:
            print(f"✗ FAIL: Text layer not found near expected position")
            return False
        
        print("\n✓ All layer composition tests passed!")
        return True
        
    finally:
        # Cleanup
        shutil.rmtree(temp_dir)

def main():
    """Run all tests."""
    print("Testing Absolute Layer Positioning")
    print("=" * 60)
    
    success = True
    
    # Run tests
    if not test_text_absolute_positioning():
        success = False
    
    if not test_layer_composition():
        success = False
    
    print("\n" + "=" * 60)
    if success:
        print("✓ ALL TESTS PASSED")
        return 0
    else:
        print("✗ SOME TESTS FAILED")
        return 1

if __name__ == '__main__':
    sys.exit(main())
