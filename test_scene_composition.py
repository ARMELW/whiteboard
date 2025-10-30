#!/usr/bin/env python3
"""
Test script for scene composition with camera viewport positioning.
This validates the compose_scene_with_camera function.
"""

import cv2
import numpy as np
import os
import sys

# Add parent directory to path to import whiteboard_animator
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from whiteboard_animator import compose_scene_with_camera

def test_basic_scene_composition():
    """Test basic scene composition with multiple layers and camera positioning."""
    print("\n" + "="*60)
    print("TEST 1: Basic Scene Composition with Camera")
    print("="*60)
    
    # Create a simple scene configuration
    scene_config = {
        'layers': [
            {
                'id': 'text_layer_1',
                'type': 'text',
                'text_config': {
                    'text': 'Hello World!',
                    'font': 'Arial',
                    'size': 80,
                    'color': (255, 0, 0),  # Red
                    'style': 'bold',
                    'align': 'center'
                },
                'position': {'x': 960, 'y': 540},  # Center of 1920x1080 scene
                'z_index': 1,
                'scale': 1.0,
                'opacity': 1.0
            },
            {
                'id': 'shape_layer_1',
                'type': 'shape',
                'shape_config': {
                    'shape': 'circle',
                    'color': (0, 255, 0),  # Green border
                    'fill_color': (200, 255, 200),  # Light green fill
                    'stroke_width': 5,
                    'position': {'x': 500, 'y': 300},
                    'size': 100
                },
                'position': {'x': 500, 'y': 300},
                'z_index': 0,
                'scale': 1.0,
                'opacity': 0.8
            },
            {
                'id': 'shape_layer_2',
                'type': 'shape',
                'shape_config': {
                    'shape': 'rectangle',
                    'color': (0, 0, 255),  # Blue border
                    'fill_color': (200, 200, 255),  # Light blue fill
                    'stroke_width': 5,
                    'position': {'x': 1400, 'y': 800},
                    'width': 200,
                    'height': 150
                },
                'position': {'x': 1400, 'y': 800},
                'z_index': 0,
                'scale': 1.0,
                'opacity': 0.8
            }
        ]
    }
    
    # Camera centered on the scene
    camera_config = {
        'width': 800,
        'height': 450,
        'position': {'x': 0.5, 'y': 0.5}  # Center
    }
    
    # Compose the scene
    result = compose_scene_with_camera(
        scene_config,
        camera_config,
        scene_width=1920,
        scene_height=1080,
        background='#FFFFFF'
    )
    
    # Save result
    output_path = 'test_scene_composition_basic.png'
    cv2.imwrite(output_path, result)
    print(f"\n✅ Test passed! Output saved to: {output_path}")
    print(f"   Image size: {result.shape[1]}x{result.shape[0]}")


def test_camera_positioning():
    """Test camera at different positions in the scene."""
    print("\n" + "="*60)
    print("TEST 2: Camera Positioning Test")
    print("="*60)
    
    # Create a scene with elements in different corners
    scene_config = {
        'layers': [
            # Top-left corner
            {
                'id': 'text_tl',
                'type': 'text',
                'text_config': {
                    'text': 'TOP LEFT',
                    'font': 'Arial',
                    'size': 50,
                    'color': (255, 0, 0),
                    'style': 'bold'
                },
                'position': {'x': 100, 'y': 100},
                'z_index': 1
            },
            # Top-right corner
            {
                'id': 'text_tr',
                'type': 'text',
                'text_config': {
                    'text': 'TOP RIGHT',
                    'font': 'Arial',
                    'size': 50,
                    'color': (0, 255, 0),
                    'style': 'bold'
                },
                'position': {'x': 1700, 'y': 100},
                'z_index': 1
            },
            # Bottom-left corner
            {
                'id': 'text_bl',
                'type': 'text',
                'text_config': {
                    'text': 'BOTTOM LEFT',
                    'font': 'Arial',
                    'size': 50,
                    'color': (0, 0, 255),
                    'style': 'bold'
                },
                'position': {'x': 100, 'y': 980},
                'z_index': 1
            },
            # Bottom-right corner
            {
                'id': 'text_br',
                'type': 'text',
                'text_config': {
                    'text': 'BOTTOM RIGHT',
                    'font': 'Arial',
                    'size': 50,
                    'color': (255, 0, 255),
                    'style': 'bold'
                },
                'position': {'x': 1600, 'y': 980},
                'z_index': 1
            },
            # Center
            {
                'id': 'text_center',
                'type': 'text',
                'text_config': {
                    'text': 'CENTER',
                    'font': 'Arial',
                    'size': 60,
                    'color': (0, 0, 0),
                    'style': 'bold'
                },
                'position': {'x': 960, 'y': 540},
                'z_index': 1
            }
        ]
    }
    
    # Test different camera positions
    camera_positions = [
        ('center', {'x': 0.5, 'y': 0.5}),
        ('top_left', {'x': 0.25, 'y': 0.25}),
        ('top_right', {'x': 0.75, 'y': 0.25}),
        ('bottom_left', {'x': 0.25, 'y': 0.75}),
        ('bottom_right', {'x': 0.75, 'y': 0.75})
    ]
    
    for name, position in camera_positions:
        camera_config = {
            'width': 800,
            'height': 450,
            'position': position
        }
        
        print(f"\n  Testing camera at {name}: {position}")
        result = compose_scene_with_camera(
            scene_config,
            camera_config,
            scene_width=1920,
            scene_height=1080,
            background='#F0F0F0'
        )
        
        output_path = f'test_scene_composition_camera_{name}.png'
        cv2.imwrite(output_path, result)
        print(f"  ✓ Saved: {output_path}")
    
    print(f"\n✅ Test passed! All camera positions rendered successfully.")


def test_layer_transformations():
    """Test layer transformations: rotation, flip, scale, opacity."""
    print("\n" + "="*60)
    print("TEST 3: Layer Transformations Test")
    print("="*60)
    
    scene_config = {
        'layers': [
            # Original
            {
                'id': 'shape_original',
                'type': 'shape',
                'shape_config': {
                    'shape': 'rectangle',
                    'color': (0, 0, 255),
                    'fill_color': (200, 200, 255),
                    'stroke_width': 3,
                    'position': {'x': 400, 'y': 300},
                    'width': 150,
                    'height': 100
                },
                'position': {'x': 400, 'y': 300},
                'z_index': 1,
                'scale': 1.0,
                'opacity': 1.0
            },
            # Rotated
            {
                'id': 'shape_rotated',
                'type': 'shape',
                'shape_config': {
                    'shape': 'rectangle',
                    'color': (255, 0, 0),
                    'fill_color': (255, 200, 200),
                    'stroke_width': 3,
                    'position': {'x': 800, 'y': 300},
                    'width': 150,
                    'height': 100
                },
                'position': {'x': 800, 'y': 300},
                'z_index': 1,
                'scale': 1.0,
                'opacity': 1.0,
                'rotation': 45
            },
            # Scaled
            {
                'id': 'shape_scaled',
                'type': 'shape',
                'shape_config': {
                    'shape': 'rectangle',
                    'color': (0, 255, 0),
                    'fill_color': (200, 255, 200),
                    'stroke_width': 3,
                    'position': {'x': 1200, 'y': 300},
                    'width': 150,
                    'height': 100
                },
                'position': {'x': 1200, 'y': 300},
                'z_index': 1,
                'scale': 1.5,
                'opacity': 1.0
            },
            # Semi-transparent
            {
                'id': 'shape_transparent',
                'type': 'shape',
                'shape_config': {
                    'shape': 'circle',
                    'color': (255, 0, 255),
                    'fill_color': (255, 200, 255),
                    'stroke_width': 3,
                    'position': {'x': 600, 'y': 700},
                    'size': 80
                },
                'position': {'x': 600, 'y': 700},
                'z_index': 1,
                'scale': 1.0,
                'opacity': 0.5
            }
        ]
    }
    
    camera_config = {
        'width': 800,
        'height': 450,
        'position': {'x': 0.5, 'y': 0.5}
    }
    
    result = compose_scene_with_camera(
        scene_config,
        camera_config,
        scene_width=1920,
        scene_height=1080,
        background='#FFFFFF'
    )
    
    output_path = 'test_scene_composition_transformations.png'
    cv2.imwrite(output_path, result)
    print(f"\n✅ Test passed! Output saved to: {output_path}")


def test_z_index_ordering():
    """Test layer z-index ordering."""
    print("\n" + "="*60)
    print("TEST 4: Z-Index Ordering Test")
    print("="*60)
    
    scene_config = {
        'layers': [
            # Bottom layer (z=0)
            {
                'id': 'layer_bottom',
                'type': 'shape',
                'shape_config': {
                    'shape': 'rectangle',
                    'color': (0, 0, 255),
                    'fill_color': (100, 100, 255),
                    'stroke_width': 3,
                    'position': {'x': 800, 'y': 500},
                    'width': 400,
                    'height': 300
                },
                'position': {'x': 800, 'y': 500},
                'z_index': 0
            },
            # Middle layer (z=1)
            {
                'id': 'layer_middle',
                'type': 'shape',
                'shape_config': {
                    'shape': 'rectangle',
                    'color': (0, 255, 0),
                    'fill_color': (100, 255, 100),
                    'stroke_width': 3,
                    'position': {'x': 900, 'y': 550},
                    'width': 350,
                    'height': 250
                },
                'position': {'x': 900, 'y': 550},
                'z_index': 1
            },
            # Top layer (z=2)
            {
                'id': 'layer_top',
                'type': 'shape',
                'shape_config': {
                    'shape': 'rectangle',
                    'color': (255, 0, 0),
                    'fill_color': (255, 100, 100),
                    'stroke_width': 3,
                    'position': {'x': 1000, 'y': 600},
                    'width': 300,
                    'height': 200
                },
                'position': {'x': 1000, 'y': 600},
                'z_index': 2
            },
            # Label
            {
                'id': 'label',
                'type': 'text',
                'text_config': {
                    'text': 'Z-Index: Red(2) > Green(1) > Blue(0)',
                    'font': 'Arial',
                    'size': 40,
                    'color': (0, 0, 0),
                    'style': 'bold'
                },
                'position': {'x': 960, 'y': 200},
                'z_index': 3
            }
        ]
    }
    
    camera_config = {
        'width': 800,
        'height': 450,
        'position': {'x': 0.5, 'y': 0.5}
    }
    
    result = compose_scene_with_camera(
        scene_config,
        camera_config,
        scene_width=1920,
        scene_height=1080,
        background='#FFFFFF'
    )
    
    output_path = 'test_scene_composition_zindex.png'
    cv2.imwrite(output_path, result)
    print(f"\n✅ Test passed! Output saved to: {output_path}")


def test_with_scene_cameras():
    """Test using sceneCameras from scene config."""
    print("\n" + "="*60)
    print("TEST 5: Scene Cameras Test")
    print("="*60)
    
    scene_config = {
        'sceneCameras': [
            {
                'id': 'camera1',
                'width': 800,
                'height': 450,
                'position': {'x': 0.3, 'y': 0.3},
                'isDefault': True
            }
        ],
        'layers': [
            {
                'id': 'text_1',
                'type': 'text',
                'text_config': {
                    'text': 'Camera focused on TOP LEFT',
                    'font': 'Arial',
                    'size': 50,
                    'color': (255, 0, 0),
                    'style': 'bold'
                },
                'position': {'x': 300, 'y': 300},
                'z_index': 1
            },
            {
                'id': 'shape_1',
                'type': 'shape',
                'shape_config': {
                    'shape': 'circle',
                    'color': (0, 0, 255),
                    'fill_color': (200, 200, 255),
                    'stroke_width': 5,
                    'position': {'x': 500, 'y': 500},
                    'size': 100
                },
                'position': {'x': 500, 'y': 500},
                'z_index': 0
            }
        ]
    }
    
    # Don't pass camera_config, let it use sceneCameras
    result = compose_scene_with_camera(
        scene_config,
        camera_config=None,
        scene_width=1920,
        scene_height=1080,
        background='#F0F0F0'
    )
    
    output_path = 'test_scene_composition_scenecameras.png'
    cv2.imwrite(output_path, result)
    print(f"\n✅ Test passed! Output saved to: {output_path}")


if __name__ == '__main__':
    print("\n" + "="*60)
    print("SCENE COMPOSITION WITH CAMERA - TEST SUITE")
    print("="*60)
    
    try:
        test_basic_scene_composition()
        test_camera_positioning()
        test_layer_transformations()
        test_z_index_ordering()
        test_with_scene_cameras()
        
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED!")
        print("="*60)
        print("\nGenerated test images:")
        print("  - test_scene_composition_basic.png")
        print("  - test_scene_composition_camera_*.png (5 files)")
        print("  - test_scene_composition_transformations.png")
        print("  - test_scene_composition_zindex.png")
        print("  - test_scene_composition_scenecameras.png")
        print("\n")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
