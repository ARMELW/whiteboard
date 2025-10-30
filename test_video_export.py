#!/usr/bin/env python3
"""
Test script for video export with camera-based scene composition.
This validates the export_scene_to_video function.
"""

import cv2
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from whiteboard_animator import export_scene_to_video


def test_basic_video_export():
    """Test basic video export with static camera."""
    print("\n" + "="*60)
    print("TEST 1: Basic Video Export (Static Camera)")
    print("="*60)
    
    scene_config = {
        'duration': 3.0,
        'layers': [
            {
                'id': 'background',
                'type': 'shape',
                'shape_config': {
                    'shape': 'rectangle',
                    'color': (200, 200, 200),
                    'fill_color': (240, 240, 250),
                    'stroke_width': 5,
                    'position': {'x': 960, 'y': 540},
                    'width': 1600,
                    'height': 800
                },
                'position': {'x': 960, 'y': 540},
                'z_index': 0
            },
            {
                'id': 'title',
                'type': 'text',
                'text_config': {
                    'text': 'Video Export Test',
                    'font': 'Arial',
                    'size': 80,
                    'color': (30, 60, 150),
                    'style': 'bold',
                    'align': 'center'
                },
                'position': {'x': 960, 'y': 400},
                'z_index': 1
            },
            {
                'id': 'circle',
                'type': 'shape',
                'shape_config': {
                    'shape': 'circle',
                    'color': (255, 0, 0),
                    'fill_color': (255, 200, 200),
                    'stroke_width': 5,
                    'position': {'x': 960, 'y': 680},
                    'size': 80
                },
                'position': {'x': 960, 'y': 680},
                'z_index': 1
            }
        ]
    }
    
    camera_config = {
        'width': 1920,
        'height': 1080,
        'position': {'x': 0.5, 'y': 0.5}
    }
    
    result = export_scene_to_video(
        scene_config,
        'test_video_basic.mp4',
        fps=30,
        camera_config=camera_config,
        scene_width=1920,
        scene_height=1080,
        background='#FFFFFF'
    )
    
    if result['success']:
        print(f"\n✅ Test passed! Video created:")
        print(f"   File: {result['output_path']}")
        print(f"   Duration: {result['duration']}s")
        print(f"   Resolution: {result['resolution']}")
        print(f"   Frames: {result['frames']}")
    else:
        print(f"\n❌ Test failed: {result.get('error', 'Unknown error')}")
        return False
    
    return True


def test_camera_pan_video():
    """Test video export with camera panning."""
    print("\n" + "="*60)
    print("TEST 2: Camera Pan Video Export")
    print("="*60)
    
    # Create a larger scene
    scene_config = {
        'duration': 5.0,
        'layers': [
            # Left marker
            {
                'id': 'left_marker',
                'type': 'shape',
                'shape_config': {
                    'shape': 'circle',
                    'color': (255, 0, 0),
                    'fill_color': (255, 200, 200),
                    'stroke_width': 5,
                    'position': {'x': 400, 'y': 540},
                    'size': 100
                },
                'position': {'x': 400, 'y': 540},
                'z_index': 1
            },
            {
                'id': 'left_text',
                'type': 'text',
                'text_config': {
                    'text': 'LEFT',
                    'font': 'Arial',
                    'size': 50,
                    'color': (0, 0, 0),
                    'style': 'bold',
                    'align': 'center'
                },
                'position': {'x': 400, 'y': 540},
                'z_index': 2
            },
            # Center marker
            {
                'id': 'center_marker',
                'type': 'shape',
                'shape_config': {
                    'shape': 'circle',
                    'color': (0, 255, 0),
                    'fill_color': (200, 255, 200),
                    'stroke_width': 5,
                    'position': {'x': 960, 'y': 540},
                    'size': 100
                },
                'position': {'x': 960, 'y': 540},
                'z_index': 1
            },
            {
                'id': 'center_text',
                'type': 'text',
                'text_config': {
                    'text': 'CENTER',
                    'font': 'Arial',
                    'size': 50,
                    'color': (0, 0, 0),
                    'style': 'bold',
                    'align': 'center'
                },
                'position': {'x': 960, 'y': 540},
                'z_index': 2
            },
            # Right marker
            {
                'id': 'right_marker',
                'type': 'shape',
                'shape_config': {
                    'shape': 'circle',
                    'color': (0, 0, 255),
                    'fill_color': (200, 200, 255),
                    'stroke_width': 5,
                    'position': {'x': 1520, 'y': 540},
                    'size': 100
                },
                'position': {'x': 1520, 'y': 540},
                'z_index': 1
            },
            {
                'id': 'right_text',
                'type': 'text',
                'text_config': {
                    'text': 'RIGHT',
                    'font': 'Arial',
                    'size': 50,
                    'color': (0, 0, 0),
                    'style': 'bold',
                    'align': 'center'
                },
                'position': {'x': 1520, 'y': 540},
                'z_index': 2
            }
        ]
    }
    
    camera_config = {
        'width': 1920,
        'height': 1080,
        'position': {'x': 0.5, 'y': 0.5}
    }
    
    # Camera pans from left to right
    camera_animation = {
        'type': 'pan',
        'start_position': {'x': 0.3, 'y': 0.5},
        'end_position': {'x': 0.7, 'y': 0.5},
        'easing': 'ease_in_out'
    }
    
    result = export_scene_to_video(
        scene_config,
        'test_video_pan.mp4',
        fps=30,
        camera_config=camera_config,
        scene_width=1920,
        scene_height=1080,
        background='#F0F0F0',
        camera_animation=camera_animation
    )
    
    if result['success']:
        print(f"\n✅ Test passed! Pan video created: {result['output_path']}")
    else:
        print(f"\n❌ Test failed: {result.get('error', 'Unknown error')}")
        return False
    
    return True


def test_camera_zoom_video():
    """Test video export with camera zoom."""
    print("\n" + "="*60)
    print("TEST 3: Camera Zoom Video Export")
    print("="*60)
    
    scene_config = {
        'duration': 4.0,
        'layers': [
            # Background
            {
                'id': 'bg',
                'type': 'shape',
                'shape_config': {
                    'shape': 'rectangle',
                    'color': (100, 100, 150),
                    'fill_color': (220, 220, 240),
                    'stroke_width': 5,
                    'position': {'x': 960, 'y': 540},
                    'width': 1600,
                    'height': 800
                },
                'position': {'x': 960, 'y': 540},
                'z_index': 0
            },
            # Center target
            {
                'id': 'target',
                'type': 'shape',
                'shape_config': {
                    'shape': 'circle',
                    'color': (255, 0, 0),
                    'fill_color': (255, 150, 150),
                    'stroke_width': 5,
                    'position': {'x': 960, 'y': 540},
                    'size': 150
                },
                'position': {'x': 960, 'y': 540},
                'z_index': 1
            },
            {
                'id': 'target_text',
                'type': 'text',
                'text_config': {
                    'text': 'ZOOM\nTARGET',
                    'font': 'Arial',
                    'size': 60,
                    'color': (255, 255, 255),
                    'style': 'bold',
                    'align': 'center'
                },
                'position': {'x': 960, 'y': 540},
                'z_index': 2
            }
        ]
    }
    
    camera_config = {
        'width': 1920,
        'height': 1080,
        'position': {'x': 0.5, 'y': 0.5}
    }
    
    # Camera zooms in from 1x to 2x
    camera_animation = {
        'type': 'zoom',
        'start_zoom': 1.0,
        'end_zoom': 2.5,
        'base_width': 1920,
        'base_height': 1080,
        'easing': 'ease_in_out'
    }
    
    result = export_scene_to_video(
        scene_config,
        'test_video_zoom.mp4',
        fps=30,
        camera_config=camera_config,
        scene_width=1920,
        scene_height=1080,
        background='#FFFFFF',
        camera_animation=camera_animation
    )
    
    if result['success']:
        print(f"\n✅ Test passed! Zoom video created: {result['output_path']}")
    else:
        print(f"\n❌ Test failed: {result.get('error', 'Unknown error')}")
        return False
    
    return True


def test_complex_scene_video():
    """Test video export with complex multi-layer scene."""
    print("\n" + "="*60)
    print("TEST 4: Complex Multi-Layer Scene Video")
    print("="*60)
    
    scene_config = {
        'duration': 3.0,
        'sceneCameras': [
            {
                'id': 'main_camera',
                'width': 1920,
                'height': 1080,
                'position': {'x': 0.5, 'y': 0.5},
                'isDefault': True
            }
        ],
        'layers': [
            # Background
            {
                'id': 'bg',
                'type': 'shape',
                'shape_config': {
                    'shape': 'rectangle',
                    'color': (150, 150, 150),
                    'fill_color': (240, 245, 250),
                    'stroke_width': 0,
                    'position': {'x': 960, 'y': 540},
                    'width': 1920,
                    'height': 1080
                },
                'position': {'x': 960, 'y': 540},
                'z_index': 0
            },
            # Title
            {
                'id': 'title',
                'type': 'text',
                'text_config': {
                    'text': 'Complex Scene Example',
                    'font': 'Arial',
                    'size': 70,
                    'color': (30, 50, 120),
                    'style': 'bold',
                    'align': 'center'
                },
                'position': {'x': 960, 'y': 150},
                'z_index': 3
            },
            # Shape 1
            {
                'id': 'shape1',
                'type': 'shape',
                'shape_config': {
                    'shape': 'rectangle',
                    'color': (255, 100, 100),
                    'fill_color': (255, 200, 200),
                    'stroke_width': 4,
                    'position': {'x': 400, 'y': 500},
                    'width': 250,
                    'height': 200
                },
                'position': {'x': 400, 'y': 500},
                'z_index': 1,
                'opacity': 0.9
            },
            # Shape 2
            {
                'id': 'shape2',
                'type': 'shape',
                'shape_config': {
                    'shape': 'circle',
                    'color': (100, 255, 100),
                    'fill_color': (200, 255, 200),
                    'stroke_width': 4,
                    'position': {'x': 960, 'y': 600},
                    'size': 120
                },
                'position': {'x': 960, 'y': 600},
                'z_index': 2,
                'opacity': 0.9
            },
            # Shape 3
            {
                'id': 'shape3',
                'type': 'shape',
                'shape_config': {
                    'shape': 'rectangle',
                    'color': (100, 100, 255),
                    'fill_color': (200, 200, 255),
                    'stroke_width': 4,
                    'position': {'x': 1520, 'y': 500},
                    'width': 250,
                    'height': 200
                },
                'position': {'x': 1520, 'y': 500},
                'z_index': 1,
                'opacity': 0.9,
                'rotation': 15
            },
            # Arrow
            {
                'id': 'arrow',
                'type': 'arrow',
                'arrow_config': {
                    'start': [400, 850],
                    'end': [1520, 850],
                    'color': (0, 0, 0),
                    'fill_color': (0, 0, 0),
                    'stroke_width': 3,
                    'arrow_size': 25
                },
                'position': {'x': 0, 'y': 0},
                'z_index': 2
            },
            # Footer text
            {
                'id': 'footer',
                'type': 'text',
                'text_config': {
                    'text': 'All layers properly positioned with camera viewport',
                    'font': 'Arial',
                    'size': 30,
                    'color': (100, 100, 100),
                    'style': 'italic',
                    'align': 'center'
                },
                'position': {'x': 960, 'y': 980},
                'z_index': 3
            }
        ]
    }
    
    result = export_scene_to_video(
        scene_config,
        'test_video_complex.mp4',
        fps=30,
        scene_width=1920,
        scene_height=1080,
        background='#FFFFFF'
    )
    
    if result['success']:
        print(f"\n✅ Test passed! Complex video created: {result['output_path']}")
    else:
        print(f"\n❌ Test failed: {result.get('error', 'Unknown error')}")
        return False
    
    return True


if __name__ == '__main__':
    print("\n" + "="*60)
    print("VIDEO EXPORT WITH CAMERA - TEST SUITE")
    print("="*60)
    
    try:
        all_passed = True
        
        if not test_basic_video_export():
            all_passed = False
        
        if not test_camera_pan_video():
            all_passed = False
        
        if not test_camera_zoom_video():
            all_passed = False
        
        if not test_complex_scene_video():
            all_passed = False
        
        if all_passed:
            print("\n" + "="*60)
            print("✅ ALL TESTS PASSED!")
            print("="*60)
            print("\nGenerated test videos:")
            print("  - test_video_basic.mp4 (3s, static camera)")
            print("  - test_video_pan.mp4 (5s, camera pan)")
            print("  - test_video_zoom.mp4 (4s, camera zoom)")
            print("  - test_video_complex.mp4 (3s, multi-layer)")
            print("\n")
        else:
            print("\n" + "="*60)
            print("❌ SOME TESTS FAILED")
            print("="*60)
            sys.exit(1)
        
    except Exception as e:
        print(f"\n❌ TEST SUITE FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
