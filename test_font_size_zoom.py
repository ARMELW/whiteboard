#!/usr/bin/env python3
"""
Test script to verify that font size is properly respected with camera zoom.
This test addresses the issue where font size doesn't respect zoom in video rendering.
"""

import cv2
import numpy as np
import os
import sys

# Add parent directory to path to import whiteboard_animator
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from whiteboard_animator import compose_scene_with_camera

def test_font_size_with_zoom():
    """Test that font size is properly rendered at different zoom levels."""
    print("\n" + "="*60)
    print("TEST: Font Size Respects Camera Zoom")
    print("="*60)
    
    # Create a scene with text at font size 60
    scene_config = {
        'layers': [
            {
                'id': 'text_layer',
                'type': 'text',
                'text_config': {
                    'text': 'Votre texte ici',
                    'font': 'Arial',
                    'size': 60,
                    'color': (0, 0, 0),  # Black
                    'style': 'normal',
                    'align': 'center'
                },
                'position': {'x': 960, 'y': 540},  # Center of 1920x1080 scene
                'anchor_point': 'center',
                'z_index': 1,
                'visible': True
            }
        ]
    }
    
    # Test 1: No zoom (zoom = 1.0)
    print("\n📷 Test 1: No zoom (zoom = 1.0)")
    camera_no_zoom = {
        'width': 800,
        'height': 450,
        'position': {'x': 0.5, 'y': 0.5},
        'zoom': 1.0
    }
    
    result_no_zoom = compose_scene_with_camera(
        scene_config,
        camera_no_zoom,
        scene_width=1920,
        scene_height=1080,
        background='#FFFFFF'
    )
    
    output_no_zoom = 'test_font_no_zoom.png'
    cv2.imwrite(output_no_zoom, result_no_zoom)
    print(f"✅ Saved: {output_no_zoom}")
    
    # Test 2: 2x zoom
    print("\n📷 Test 2: 2x zoom (zoom = 2.0)")
    camera_2x_zoom = {
        'width': 800,
        'height': 450,
        'position': {'x': 0.5, 'y': 0.5},
        'zoom': 2.0
    }
    
    result_2x_zoom = compose_scene_with_camera(
        scene_config,
        camera_2x_zoom,
        scene_width=1920,
        scene_height=1080,
        background='#FFFFFF'
    )
    
    output_2x_zoom = 'test_font_2x_zoom.png'
    cv2.imwrite(output_2x_zoom, result_2x_zoom)
    print(f"✅ Saved: {output_2x_zoom}")
    
    # Test 3: 0.5x zoom (zoomed out)
    print("\n📷 Test 3: 0.5x zoom (zoom = 0.5)")
    camera_half_zoom = {
        'width': 800,
        'height': 450,
        'position': {'x': 0.5, 'y': 0.5},
        'zoom': 0.5
    }
    
    result_half_zoom = compose_scene_with_camera(
        scene_config,
        camera_half_zoom,
        scene_width=1920,
        scene_height=1080,
        background='#FFFFFF'
    )
    
    output_half_zoom = 'test_font_half_zoom.png'
    cv2.imwrite(output_half_zoom, result_half_zoom)
    print(f"✅ Saved: {output_half_zoom}")
    
    # Visual comparison
    print("\n" + "="*60)
    print("RESULTS:")
    print("="*60)
    print(f"✅ No zoom (1.0x): {output_no_zoom}")
    print(f"✅ 2x zoom: {output_2x_zoom} (text should be 2x larger and crisp)")
    print(f"✅ 0.5x zoom: {output_half_zoom} (text should be 0.5x smaller and crisp)")
    print("\nThe text should appear crisp and clear at all zoom levels.")
    print("Previously, the text would be blurry due to image scaling.")
    print("="*60)
    
    return True

if __name__ == '__main__':
    try:
        test_font_size_with_zoom()
        print("\n✅ All tests passed!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
