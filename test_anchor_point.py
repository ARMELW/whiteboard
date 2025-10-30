#!/usr/bin/env python3
"""
Test script to verify anchor_point functionality for layers.
Tests that layers can be positioned using center or top-left anchor points.
"""

import json
import os
import sys
import tempfile
import shutil

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from whiteboard_animator import compose_layers, render_text_to_image, render_shape_to_image
import numpy as np
import cv2

def create_test_image(width, height, color):
    """Create a simple test image with a colored rectangle."""
    img = np.ones((height, width, 3), dtype=np.uint8) * 255
    # Draw a colored rectangle in the center
    margin = 10
    cv2.rectangle(img, (margin, margin), (width - margin, height - margin), color, -1)
    return img

def test_anchor_point_top_left():
    """Test that anchor_point='top-left' positions layer at top-left corner."""
    print("=" * 60)
    print("Testing anchor_point='top-left' (default behavior)")
    print("=" * 60)
    
    target_width = 400
    target_height = 300
    
    # Create a test image
    test_img_path = tempfile.mktemp(suffix='.png')
    test_img = create_test_image(100, 80, (0, 0, 255))  # Red image in BGR format
    cv2.imwrite(test_img_path, test_img)
    
    try:
        # Position at (50, 50) with top-left anchor
        layers = [
            {
                'image_path': test_img_path,
                'position': {'x': 50, 'y': 50},
                'anchor_point': 'top-left',
                'z_index': 1
            }
        ]
        
        result = compose_layers(layers, target_width, target_height)
        
        # Check that the top-left corner of the colored area is at (60, 60) (50 + 10 margin)
        pixel_at_corner = result[60, 60]
        # BGR format, so red should be (0, 0, 255)
        is_red = (pixel_at_corner[2] > 200 and pixel_at_corner[0] < 50 and pixel_at_corner[1] < 50)
        
        if is_red:
            print("✓ PASS: Layer positioned with top-left anchor at (50, 50)")
            return True
        else:
            print(f"✗ FAIL: Expected red at (60, 60), got {pixel_at_corner}")
            return False
    finally:
        if os.path.exists(test_img_path):
            os.remove(test_img_path)

def test_anchor_point_center():
    """Test that anchor_point='center' positions layer at center."""
    print("\n" + "=" * 60)
    print("Testing anchor_point='center'")
    print("=" * 60)
    
    target_width = 400
    target_height = 300
    
    # Create a test image (100x80)
    test_img_path = tempfile.mktemp(suffix='.png')
    test_img = create_test_image(100, 80, (0, 255, 0))  # Green image in BGR format
    cv2.imwrite(test_img_path, test_img)
    
    try:
        # Position at center (200, 150) with center anchor
        # With center anchor, the image should be positioned such that its center is at (200, 150)
        # Image is 100x80, so top-left should be at (150, 110) = (200-50, 150-40)
        layers = [
            {
                'image_path': test_img_path,
                'position': {'x': 200, 'y': 150},
                'anchor_point': 'center',
                'z_index': 1
            }
        ]
        
        result = compose_layers(layers, target_width, target_height)
        
        # Check that the center of the image is at (200, 150)
        # The colored area starts at 10px margin, so actual center is at image (50, 40)
        # Which translates to canvas position (150+50, 110+40) = (200, 150)
        pixel_at_center = result[150, 200]
        is_green = (pixel_at_center[1] > 200 and pixel_at_center[0] < 50 and pixel_at_center[2] < 50)
        
        # Also check that top-left is at expected position (160, 120) = (150+10, 110+10)
        pixel_at_top_left = result[120, 160]
        is_green_tl = (pixel_at_top_left[1] > 200 and pixel_at_top_left[0] < 50 and pixel_at_top_left[2] < 50)
        
        if is_green and is_green_tl:
            print("✓ PASS: Layer positioned with center anchor at (200, 150)")
            return True
        else:
            print(f"✗ FAIL: Expected green at center (150, 200) and top-left (120, 160)")
            print(f"  Center pixel: {pixel_at_center}, Top-left pixel: {pixel_at_top_left}")
            return False
    finally:
        if os.path.exists(test_img_path):
            os.remove(test_img_path)

def test_anchor_point_with_width_height():
    """Test that anchor_point works correctly with explicit width/height."""
    print("\n" + "=" * 60)
    print("Testing anchor_point with explicit width/height")
    print("=" * 60)
    
    target_width = 400
    target_height = 300
    
    # Create a test image (original 100x80)
    test_img_path = tempfile.mktemp(suffix='.png')
    test_img = create_test_image(100, 80, (255, 0, 0))  # Blue image in BGR format
    cv2.imwrite(test_img_path, test_img)
    
    try:
        # Position at (200, 150) with center anchor and resize to 80x60
        # With center anchor and 80x60 size, top-left should be at (160, 120) = (200-40, 150-30)
        layers = [
            {
                'image_path': test_img_path,
                'position': {'x': 200, 'y': 150},
                'anchor_point': 'center',
                'width': 80,
                'height': 60,
                'z_index': 1
            }
        ]
        
        result = compose_layers(layers, target_width, target_height)
        
        # Check that the center is at (200, 150)
        pixel_at_center = result[150, 200]
        # BGR format, blue should be (255, 0, 0)
        is_blue = (pixel_at_center[0] > 200 and pixel_at_center[1] < 50 and pixel_at_center[2] < 50)
        
        # Check that top-left colored area is at expected position
        # Top-left of image: (160, 120)
        # Top-left of colored area: (160+10*0.8, 120+10*0.75) ≈ (168, 128)
        pixel_near_tl = result[128, 168]
        is_blue_tl = (pixel_near_tl[0] > 200 and pixel_near_tl[1] < 50 and pixel_near_tl[2] < 50)
        
        if is_blue and is_blue_tl:
            print("✓ PASS: Layer with explicit width/height positioned correctly with center anchor")
            return True
        else:
            print(f"✗ FAIL: Expected blue at center and top-left")
            print(f"  Center pixel (150, 200): {pixel_at_center}")
            print(f"  Near top-left pixel (128, 168): {pixel_near_tl}")
            return False
    finally:
        if os.path.exists(test_img_path):
            os.remove(test_img_path)

def test_text_layer_anchor_point():
    """Test that text layers respect anchor_point."""
    print("\n" + "=" * 60)
    print("Testing text layer with anchor_point")
    print("=" * 60)
    
    target_width = 400
    target_height = 300
    
    # Test with center anchor point
    layers = [
        {
            'type': 'text',
            'text_config': {
                'text': 'TEST',
                'font': 'Arial',
                'size': 48,
                'color': [255, 0, 0],
                'position': {'x': 200, 'y': 150}
            },
            'position': {'x': 200, 'y': 150},
            'anchor_point': 'center',
            'z_index': 1
        }
    ]
    
    result = compose_layers(layers, target_width, target_height)
    
    # Find non-white pixels around the center
    center_region = result[140:160, 190:210]
    has_text = np.any(center_region < 250)
    
    if has_text:
        print("✓ PASS: Text layer with center anchor has content near center")
        return True
    else:
        print("✗ FAIL: No text found near center position")
        return False

def test_shape_layer_anchor_point():
    """Test that shape layers respect anchor_point."""
    print("\n" + "=" * 60)
    print("Testing shape layer with anchor_point")
    print("=" * 60)
    
    target_width = 400
    target_height = 300
    
    # Test circle with center anchor point
    layers = [
        {
            'type': 'shape',
            'shape_config': {
                'shape': 'circle',
                'color': [0, 255, 0],
                'fill_color': [0, 255, 0],
                'size': 50,
                'position': {'x': 200, 'y': 150}
            },
            'position': {'x': 200, 'y': 150},
            'anchor_point': 'center',
            'z_index': 1
        }
    ]
    
    result = compose_layers(layers, target_width, target_height)
    
    # Check that there's green color at the center
    pixel_at_center = result[150, 200]
    is_green = (pixel_at_center[1] > 200 and pixel_at_center[0] < 50 and pixel_at_center[2] < 50)
    
    if is_green:
        print("✓ PASS: Shape layer with center anchor positioned correctly")
        return True
    else:
        print(f"✗ FAIL: Expected green at center (150, 200), got {pixel_at_center}")
        return False

def test_backwards_compatibility():
    """Test that layers without anchor_point still work (default top-left)."""
    print("\n" + "=" * 60)
    print("Testing backwards compatibility (no anchor_point specified)")
    print("=" * 60)
    
    target_width = 400
    target_height = 300
    
    # Create a test image
    test_img_path = tempfile.mktemp(suffix='.png')
    test_img = create_test_image(100, 80, (0, 165, 255))  # Orange image in BGR format
    cv2.imwrite(test_img_path, test_img)
    
    try:
        # Position at (50, 50) WITHOUT anchor_point (should default to top-left)
        layers = [
            {
                'image_path': test_img_path,
                'position': {'x': 50, 'y': 50},
                'z_index': 1
            }
        ]
        
        result = compose_layers(layers, target_width, target_height)
        
        # Check that the top-left corner of the colored area is at (60, 60)
        pixel_at_corner = result[60, 60]
        # BGR format, orange should be (0, 165, 255)
        is_orange = (pixel_at_corner[2] > 200 and pixel_at_corner[1] > 100 and pixel_at_corner[0] < 50)
        
        if is_orange:
            print("✓ PASS: Backwards compatibility maintained (defaults to top-left)")
            return True
        else:
            print(f"✗ FAIL: Expected orange at (60, 60), got {pixel_at_corner}")
            return False
    finally:
        if os.path.exists(test_img_path):
            os.remove(test_img_path)

def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("ANCHOR POINT POSITIONING TESTS")
    print("=" * 60)
    
    tests = [
        test_anchor_point_top_left,
        test_anchor_point_center,
        test_anchor_point_with_width_height,
        test_text_layer_anchor_point,
        test_shape_layer_anchor_point,
        test_backwards_compatibility,
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"✗ FAIL: Test raised exception: {e}")
            import traceback
            traceback.print_exc()
            results.append(False)
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Passed: {sum(results)}/{len(results)}")
    print(f"Failed: {len(results) - sum(results)}/{len(results)}")
    
    if all(results):
        print("\n✓ ALL TESTS PASSED")
        return 0
    else:
        print("\n✗ SOME TESTS FAILED")
        return 1

if __name__ == '__main__':
    sys.exit(main())
