#!/usr/bin/env python3
"""
Demo: Video Export with Camera-Based Scene Composition
Shows practical examples of exporting scenes to video.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from whiteboard_animator import export_scene_to_video


def demo_simple_video():
    """Create a simple video with static camera."""
    print("\n" + "="*60)
    print("DEMO 1: Simple Video (2 seconds)")
    print("="*60)
    
    scene_config = {
        'duration': 2.0,
        'layers': [
            {
                'id': 'title',
                'type': 'text',
                'text_config': {
                    'text': 'Hello Video!',
                    'font': 'Arial',
                    'size': 100,
                    'color': (50, 100, 200),
                    'style': 'bold',
                    'align': 'center'
                },
                'position': {'x': 960, 'y': 540},
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
        'demo_simple.mp4',
        fps=30,
        camera_config=camera_config,
        scene_width=1920,
        scene_height=1080
    )
    
    if result['success']:
        print(f"✅ Video created: {result['output_path']}")
    else:
        print(f"❌ Failed: {result.get('error')}")


def demo_camera_movement():
    """Create a video with camera panning."""
    print("\n" + "="*60)
    print("DEMO 2: Camera Pan Video (3 seconds)")
    print("="*60)
    
    scene_config = {
        'duration': 3.0,
        'layers': [
            {
                'id': 'left',
                'type': 'text',
                'text_config': {
                    'text': 'LEFT',
                    'font': 'Arial',
                    'size': 80,
                    'color': (255, 0, 0),
                    'style': 'bold'
                },
                'position': {'x': 480, 'y': 540},
                'z_index': 1
            },
            {
                'id': 'right',
                'type': 'text',
                'text_config': {
                    'text': 'RIGHT',
                    'font': 'Arial',
                    'size': 80,
                    'color': (0, 0, 255),
                    'style': 'bold'
                },
                'position': {'x': 1440, 'y': 540},
                'z_index': 1
            }
        ]
    }
    
    camera_config = {
        'width': 1920,
        'height': 1080,
        'position': {'x': 0.5, 'y': 0.5}
    }
    
    camera_animation = {
        'type': 'pan',
        'start_position': {'x': 0.3, 'y': 0.5},
        'end_position': {'x': 0.7, 'y': 0.5},
        'easing': 'ease_in_out'
    }
    
    result = export_scene_to_video(
        scene_config,
        'demo_pan.mp4',
        fps=30,
        camera_config=camera_config,
        scene_width=1920,
        scene_height=1080,
        camera_animation=camera_animation
    )
    
    if result['success']:
        print(f"✅ Video created: {result['output_path']}")
    else:
        print(f"❌ Failed: {result.get('error')}")


if __name__ == '__main__':
    print("\n" + "="*60)
    print("  VIDEO EXPORT DEMO")
    print("="*60)
    
    try:
        demo_simple_video()
        demo_camera_movement()
        
        print("\n" + "="*60)
        print("✅ ALL DEMOS COMPLETED!")
        print("="*60)
        print("\nGenerated videos:")
        print("  - demo_simple.mp4 (2s, static)")
        print("  - demo_pan.mp4 (3s, camera pan)")
        print("\n")
        
    except Exception as e:
        print(f"\n❌ DEMO FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
