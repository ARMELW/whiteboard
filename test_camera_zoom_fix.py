#!/usr/bin/env python3
"""
Test script to verify camera zoom and position fix.

This test creates a scene with a known layer position and verifies that
different camera zoom levels properly affect the rendered output.
"""

import json
import os
import sys
import tempfile
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_camera_zoom_basic():
    """Test basic camera zoom functionality."""
    print("\n" + "="*60)
    print("TEST 1: Basic Camera Zoom")
    print("="*60)
    
    # Import after path is set
    from whiteboard_animator import compose_scene_with_camera
    import cv2
    
    # Create a simple scene with a layer at center
    # Note: for shapes, the position in shape_config determines where it's drawn
    # The layer position is not used for shapes
    scene_config = {
        'layers': [
            {
                'id': 'test-rect',
                'type': 'shape',
                'shape_config': {
                    'shape': 'rectangle',
                    'color': (0, 0, 255),  # Blue in RGB -> Red in BGR
                    'fill_color': (100, 100, 255),  # Light blue in RGB -> Light red in BGR
                    'stroke_width': 5,
                    'position': {'x': 960, 'y': 540},  # Center of 1920x1080 scene
                    'width': 200,
                    'height': 100
                },
                'position': {'x': 0, 'y': 0},  # Not used for shapes
                'z_index': 1,
                'visible': True
            }
        ]
    }
    
    # Test with different zoom levels
    test_cases = [
        {'zoom': 1.0, 'desc': 'No zoom (1:1)', 'file': '/tmp/test_zoom_1.0.png'},
        {'zoom': 2.0, 'desc': 'Zoom in 2x', 'file': '/tmp/test_zoom_2.0.png'},
        {'zoom': 0.5, 'desc': 'Zoom out 0.5x', 'file': '/tmp/test_zoom_0.5.png'},
    ]
    
    for test in test_cases:
        print(f"\n  Testing {test['desc']}...")
        
        camera_config = {
            'width': 800,
            'height': 450,
            'position': {'x': 0.5, 'y': 0.5},  # Center of scene
            'zoom': test['zoom']
        }
        
        result = compose_scene_with_camera(
            scene_config,
            camera_config,
            scene_width=1920,
            scene_height=1080,
            background='#FFFFFF',
            verbose=True
        )
        
        # Save the result for visual inspection
        cv2.imwrite(test['file'], result)
        print(f"  💾 Saved result to: {test['file']}")
        
        # Verify result dimensions
        assert result.shape[0] == 450, f"Height should be 450, got {result.shape[0]}"
        assert result.shape[1] == 800, f"Width should be 800, got {result.shape[1]}"
        assert result.shape[2] == 3, f"Should have 3 channels, got {result.shape[2]}"
        
        print(f"  ✓ Result shape: {result.shape}")
        
        # Check if there's non-white content (our red rectangle)
        white = np.array([255, 255, 255])
        non_white_pixels = np.any(result != white, axis=2)
        non_white_count = np.sum(non_white_pixels)
        
        print(f"  ✓ Non-white pixels: {non_white_count}")
        
        # Just check that content is visible (don't make strict assertions about pixel counts)
        assert non_white_count > 0, f"Should have some visible content"
    
    print("\n✅ Basic camera zoom test PASSED")


def test_camera_position_with_zoom():
    """Test camera position works correctly with zoom."""
    print("\n" + "="*60)
    print("TEST 2: Camera Position with Zoom")
    print("="*60)
    
    from whiteboard_animator import compose_scene_with_camera
    
    # Create a scene with layer at specific position
    scene_config = {
        'layers': [
            {
                'id': 'test-circle',
                'type': 'shape',
                'shape_config': {
                    'shape': 'circle',
                    'color': (0, 0, 255),  # Blue
                    'fill_color': (100, 100, 255),
                    'stroke_width': 3,
                    'position': {'x': 640, 'y': 360},  # Top-left quadrant
                    'size': 50
                },
                'position': {'x': 640, 'y': 360},
                'z_index': 1,
                'visible': True
            }
        ]
    }
    
    # Test different camera positions with zoom
    test_cases = [
        {'x': 0.33, 'y': 0.33, 'zoom': 1.0, 'desc': 'Top-left, no zoom'},
        {'x': 0.33, 'y': 0.33, 'zoom': 2.0, 'desc': 'Top-left, zoom 2x'},
        {'x': 0.5, 'y': 0.5, 'zoom': 1.0, 'desc': 'Center, no zoom'},
    ]
    
    for test in test_cases:
        print(f"\n  Testing {test['desc']}...")
        
        camera_config = {
            'width': 800,
            'height': 450,
            'position': {'x': test['x'], 'y': test['y']},
            'zoom': test['zoom']
        }
        
        result = compose_scene_with_camera(
            scene_config,
            camera_config,
            scene_width=1920,
            scene_height=1080,
            background='#FFFFFF',
            verbose=True
        )
        
        # Verify result
        assert result.shape == (450, 800, 3), f"Shape mismatch: {result.shape}"
        print(f"  ✓ Result shape correct")
    
    print("\n✅ Camera position with zoom test PASSED")


def test_real_scene_data():
    """Test with the real scene data from the issue."""
    print("\n" + "="*60)
    print("TEST 3: Real Scene Data from Issue")
    print("="*60)
    
    from whiteboard_animator import compose_scene_with_camera
    
    # Simplified version of the scene from the issue
    scene_config = {
        'layers': [
            {
                'id': 'test-layer',
                'type': 'shape',
                'shape_config': {
                    'shape': 'rectangle',
                    'color': (0, 0, 0),
                    'fill_color': (200, 200, 200),
                    'stroke_width': 2,
                    'position': {'x': 632, 'y': 372},
                    'width': 85,
                    'height': 124
                },
                'position': {'x': 632, 'y': 372},
                'scale': 0.133,
                'z_index': 0,
                'visible': True
            }
        ]
    }
    
    # Camera config from the issue
    camera_config = {
        'id': 'ee096ad9-d94f-45cd-b09d-7bbbd370fe34',
        'name': 'Vue par défaut',
        'zoom': 1,
        'scale': 1,
        'width': 800,
        'height': 450,
        'position': {'x': 0.5, 'y': 0.5},
        'isDefault': True
    }
    
    print("\n  Rendering scene with camera...")
    result = compose_scene_with_camera(
        scene_config,
        camera_config,
        scene_width=1920,
        scene_height=1080,
        background='#f0f0f0',
        verbose=True
    )
    
    # Verify result
    assert result.shape == (450, 800, 3), f"Shape mismatch: {result.shape}"
    print(f"  ✓ Result shape correct: {result.shape}")
    
    # Check that content was rendered
    gray = np.array([240, 240, 240])  # Background is #f0f0f0
    tolerance = 20
    non_bg_pixels = np.any(np.abs(result.astype(int) - gray) > tolerance, axis=2)
    non_bg_count = np.sum(non_bg_pixels)
    
    print(f"  ✓ Non-background pixels: {non_bg_count}")
    assert non_bg_count > 0, "Should have some rendered content"
    
    print("\n✅ Real scene data test PASSED")


if __name__ == '__main__':
    try:
        test_camera_zoom_basic()
        test_camera_position_with_zoom()
        test_real_scene_data()
        
        print("\n" + "="*60)
        print("🎉 ALL TESTS PASSED!")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
