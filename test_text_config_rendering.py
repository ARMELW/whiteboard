#!/usr/bin/env python3
"""Test script to verify that text layer config is properly applied when rendering."""

import sys
import os
import cv2
import numpy as np

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from whiteboard_animator import compose_layers, render_text_to_image

def test_text_config_applied():
    """Test that text config (color, font size) is actually applied in rendering."""
    print("Testing text config rendering with color...")
    
    # Create a text layer with RED color
    text_config = {
        'text': 'Hello World',
        'font': 'DejaVuSans',
        'size': 80,
        'color': [0, 0, 255],  # RED in BGR
        'style': 'bold',
        'align': 'center'
    }
    
    # Render the text
    img = render_text_to_image(text_config, 800, 600)
    
    if img is None:
        print("✗ Failed to render text")
        return False
    
    # Check if the image has red pixels (non-white)
    # Text should be red (0, 0, 255) in BGR
    red_mask = (img[:, :, 2] > 200) & (img[:, :, 0] < 50) & (img[:, :, 1] < 50)
    red_pixel_count = np.sum(red_mask)
    
    print(f"  Red pixels found: {red_pixel_count}")
    
    if red_pixel_count > 100:  # Should have some red pixels
        print("✓ Text rendered with correct color (red)")
        cv2.imwrite("/tmp/test_text_red.png", img)
        return True
    else:
        print("✗ Text did NOT render with correct color")
        cv2.imwrite("/tmp/test_text_red_failed.png", img)
        return False

def test_text_layer_compose_with_config():
    """Test that text layers in compose_layers preserve config."""
    print("\nTesting text layer composition with color config...")
    
    # Test with a text layer with BLUE color
    layers_config = [
        {
            'type': 'text',
            'z_index': 1,
            'text_config': {
                'text': 'Blue Text',
                'font': 'DejaVuSans',
                'size': 60,
                'color': [255, 0, 0],  # BLUE in BGR
                'style': 'bold'
            }
        }
    ]
    
    # Compose layers
    result = compose_layers(layers_config, 800, 600)
    
    if result is None:
        print("✗ Failed to compose layers")
        return False
    
    # Check if the result has blue pixels
    blue_mask = (result[:, :, 0] > 200) & (result[:, :, 1] < 50) & (result[:, :, 2] < 50)
    blue_pixel_count = np.sum(blue_mask)
    
    print(f"  Blue pixels found: {blue_pixel_count}")
    
    if blue_pixel_count > 100:  # Should have some blue pixels
        print("✓ Text layer composed with correct color (blue)")
        cv2.imwrite("/tmp/test_layer_blue.png", result)
        return True
    else:
        print("✗ Text layer did NOT compose with correct color")
        cv2.imwrite("/tmp/test_layer_blue_failed.png", result)
        return False

def test_multiple_text_layers_with_different_configs():
    """Test multiple text layers with different colors and sizes."""
    print("\nTesting multiple text layers with different configs...")
    
    layers_config = [
        {
            'type': 'text',
            'z_index': 1,
            'text_config': {
                'text': 'Red Text',
                'font': 'DejaVuSans',
                'size': 48,
                'color': [0, 0, 255],  # RED
                'position': {'x': 100, 'y': 100}
            }
        },
        {
            'type': 'text',
            'z_index': 2,
            'text_config': {
                'text': 'Green Text',
                'font': 'DejaVuSans',
                'size': 36,
                'color': [0, 255, 0],  # GREEN
                'position': {'x': 100, 'y': 300}
            }
        },
        {
            'type': 'text',
            'z_index': 3,
            'text_config': {
                'text': 'Blue Text',
                'font': 'DejaVuSans',
                'size': 52,
                'color': [255, 0, 0],  # BLUE
                'position': {'x': 100, 'y': 450}
            }
        }
    ]
    
    result = compose_layers(layers_config, 800, 600)
    
    if result is None:
        print("✗ Failed to compose layers")
        return False
    
    # Check for each color
    red_mask = (result[:, :, 2] > 200) & (result[:, :, 0] < 50) & (result[:, :, 1] < 50)
    green_mask = (result[:, :, 1] > 200) & (result[:, :, 0] < 50) & (result[:, :, 2] < 50)
    blue_mask = (result[:, :, 0] > 200) & (result[:, :, 1] < 50) & (result[:, :, 2] < 50)
    
    red_count = np.sum(red_mask)
    green_count = np.sum(green_mask)
    blue_count = np.sum(blue_mask)
    
    print(f"  Red pixels: {red_count}, Green pixels: {green_count}, Blue pixels: {blue_count}")
    
    all_colors_present = red_count > 100 and green_count > 100 and blue_count > 100
    
    if all_colors_present:
        print("✓ All text layers rendered with their respective colors")
        cv2.imwrite("/tmp/test_multiple_layers.png", result)
        return True
    else:
        print("✗ Some text layers did NOT render with correct colors")
        cv2.imwrite("/tmp/test_multiple_layers_failed.png", result)
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Text Config Rendering Tests")
    print("=" * 60)
    
    tests = [
        test_text_config_applied,
        test_text_layer_compose_with_config,
        test_multiple_text_layers_with_different_configs
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
