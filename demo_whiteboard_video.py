#!/usr/bin/env python3
"""
Demo: Whiteboard-Style Video Export with Progressive Drawing Animation
Shows how to export scenes with drawing hand animation.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from whiteboard_animator import export_scene_to_whiteboard_video


def demo_simple_whiteboard():
    """Create a simple whiteboard video with text being written."""
    print("\n" + "="*60)
    print("DEMO 1: Simple Whiteboard with Text")
    print("="*60)
    
    scene_config = {
        'layers': [
            {
                'id': 'title',
                'type': 'text',
                'text_config': {
                    'text': 'Hello Whiteboard!',
                    'font': 'Arial',
                    'size': 100,
                    'color': (50, 50, 200),
                    'style': 'bold',
                    'align': 'center'
                },
                'position': {'x': 960, 'y': 400},
                'z_index': 1,
                'draw_duration': 2.0
            },
            {
                'id': 'subtitle',
                'type': 'text',
                'text_config': {
                    'text': 'Animated Drawing',
                    'font': 'Arial',
                    'size': 60,
                    'color': (100, 100, 100),
                    'style': 'italic',
                    'align': 'center'
                },
                'position': {'x': 960, 'y': 650},
                'z_index': 2,
                'draw_duration': 1.5
            }
        ]
    }
    
    camera_config = {
        'width': 1920,
        'height': 1080,
        'position': {'x': 0.5, 'y': 0.5}
    }
    
    result = export_scene_to_whiteboard_video(
        scene_config,
        'demo_whiteboard_simple.mp4',
        fps=30,
        camera_config=camera_config,
        scene_width=1920,
        scene_height=1080,
        show_hand=True,
        final_hold_duration=2.0
    )
    
    if result['success']:
        print(f"\n✅ Video created: {result['output_path']}")
        print(f"   Duration: {result['duration']:.1f}s")
    else:
        print(f"\n❌ Failed: {result.get('error')}")


def demo_shapes_whiteboard():
    """Create a whiteboard video with shapes being drawn."""
    print("\n" + "="*60)
    print("DEMO 2: Whiteboard with Shapes")
    print("="*60)
    
    scene_config = {
        'layers': [
            # Title
            {
                'id': 'title',
                'type': 'text',
                'text_config': {
                    'text': 'Drawing Shapes',
                    'font': 'Arial',
                    'size': 70,
                    'color': (30, 60, 120),
                    'style': 'bold',
                    'align': 'center'
                },
                'position': {'x': 960, 'y': 150},
                'z_index': 0,
                'draw_duration': 1.5
            },
            # Circle
            {
                'id': 'circle',
                'type': 'shape',
                'shape_config': {
                    'shape': 'circle',
                    'color': (255, 0, 0),
                    'fill_color': (255, 200, 200),
                    'stroke_width': 5,
                    'position': {'x': 400, 'y': 500},
                    'size': 120
                },
                'position': {'x': 400, 'y': 500},
                'z_index': 1,
                'draw_duration': 2.0
            },
            # Rectangle
            {
                'id': 'rectangle',
                'type': 'shape',
                'shape_config': {
                    'shape': 'rectangle',
                    'color': (0, 255, 0),
                    'fill_color': (200, 255, 200),
                    'stroke_width': 5,
                    'position': {'x': 960, 'y': 600},
                    'width': 250,
                    'height': 180
                },
                'position': {'x': 960, 'y': 600},
                'z_index': 2,
                'draw_duration': 2.0
            },
            # Triangle (using shape)
            {
                'id': 'triangle',
                'type': 'shape',
                'shape_config': {
                    'shape': 'triangle',
                    'color': (0, 0, 255),
                    'fill_color': (200, 200, 255),
                    'stroke_width': 5,
                    'position': {'x': 1520, 'y': 500},
                    'size': 140
                },
                'position': {'x': 1520, 'y': 500},
                'z_index': 3,
                'draw_duration': 2.0
            }
        ]
    }
    
    camera_config = {
        'width': 1920,
        'height': 1080,
        'position': {'x': 0.5, 'y': 0.5}
    }
    
    result = export_scene_to_whiteboard_video(
        scene_config,
        'demo_whiteboard_shapes.mp4',
        fps=30,
        camera_config=camera_config,
        scene_width=1920,
        scene_height=1080,
        show_hand=True,
        final_hold_duration=2.0
    )
    
    if result['success']:
        print(f"\n✅ Video created: {result['output_path']}")
        print(f"   Duration: {result['duration']:.1f}s")
    else:
        print(f"\n❌ Failed: {result.get('error')}")


def demo_complex_whiteboard():
    """Create a complex whiteboard video with multiple elements."""
    print("\n" + "="*60)
    print("DEMO 3: Complex Whiteboard Scene")
    print("="*60)
    
    scene_config = {
        'layers': [
            # Background box
            {
                'id': 'bg_box',
                'type': 'shape',
                'shape_config': {
                    'shape': 'rectangle',
                    'color': (200, 200, 200),
                    'fill_color': (245, 245, 250),
                    'stroke_width': 3,
                    'position': {'x': 960, 'y': 650},
                    'width': 1700,
                    'height': 700
                },
                'position': {'x': 960, 'y': 650},
                'z_index': 0,
                'draw_duration': 1.0
            },
            # Title
            {
                'id': 'title',
                'type': 'text',
                'text_config': {
                    'text': 'Whiteboard Video',
                    'font': 'Arial',
                    'size': 80,
                    'color': (30, 50, 120),
                    'style': 'bold',
                    'align': 'center'
                },
                'position': {'x': 960, 'y': 200},
                'z_index': 1,
                'draw_duration': 1.5
            },
            # Bullet point 1
            {
                'id': 'bullet1',
                'type': 'shape',
                'shape_config': {
                    'shape': 'circle',
                    'color': (50, 150, 50),
                    'fill_color': (150, 255, 150),
                    'stroke_width': 3,
                    'position': {'x': 300, 'y': 450},
                    'size': 25
                },
                'position': {'x': 300, 'y': 450},
                'z_index': 2,
                'draw_duration': 0.5
            },
            {
                'id': 'text1',
                'type': 'text',
                'text_config': {
                    'text': 'Progressive drawing animation',
                    'font': 'Arial',
                    'size': 40,
                    'color': (0, 0, 0)
                },
                'position': {'x': 400, 'y': 450},
                'z_index': 2,
                'draw_duration': 1.2
            },
            # Bullet point 2
            {
                'id': 'bullet2',
                'type': 'shape',
                'shape_config': {
                    'shape': 'circle',
                    'color': (50, 150, 50),
                    'fill_color': (150, 255, 150),
                    'stroke_width': 3,
                    'position': {'x': 300, 'y': 600},
                    'size': 25
                },
                'position': {'x': 300, 'y': 600},
                'z_index': 3,
                'draw_duration': 0.5
            },
            {
                'id': 'text2',
                'type': 'text',
                'text_config': {
                    'text': 'Camera-based positioning',
                    'font': 'Arial',
                    'size': 40,
                    'color': (0, 0, 0)
                },
                'position': {'x': 400, 'y': 600},
                'z_index': 3,
                'draw_duration': 1.2
            },
            # Bullet point 3
            {
                'id': 'bullet3',
                'type': 'shape',
                'shape_config': {
                    'shape': 'circle',
                    'color': (50, 150, 50),
                    'fill_color': (150, 255, 150),
                    'stroke_width': 3,
                    'position': {'x': 300, 'y': 750},
                    'size': 25
                },
                'position': {'x': 300, 'y': 750},
                'z_index': 4,
                'draw_duration': 0.5
            },
            {
                'id': 'text3',
                'type': 'text',
                'text_config': {
                    'text': 'Multiple layer support',
                    'font': 'Arial',
                    'size': 40,
                    'color': (0, 0, 0)
                },
                'position': {'x': 400, 'y': 750},
                'z_index': 4,
                'draw_duration': 1.2
            },
            # Arrow
            {
                'id': 'arrow',
                'type': 'arrow',
                'arrow_config': {
                    'start': [400, 900],
                    'end': [1520, 900],
                    'color': (0, 0, 0),
                    'fill_color': (0, 0, 0),
                    'stroke_width': 3,
                    'arrow_size': 25
                },
                'position': {'x': 0, 'y': 0},
                'z_index': 5,
                'draw_duration': 1.5
            }
        ]
    }
    
    camera_config = {
        'width': 1920,
        'height': 1080,
        'position': {'x': 0.5, 'y': 0.5}
    }
    
    result = export_scene_to_whiteboard_video(
        scene_config,
        'demo_whiteboard_complex.mp4',
        fps=30,
        camera_config=camera_config,
        scene_width=1920,
        scene_height=1080,
        show_hand=True,
        final_hold_duration=2.0
    )
    
    if result['success']:
        print(f"\n✅ Video created: {result['output_path']}")
        print(f"   Duration: {result['duration']:.1f}s")
    else:
        print(f"\n❌ Failed: {result.get('error')}")


if __name__ == '__main__':
    print("\n" + "="*60)
    print("  WHITEBOARD VIDEO EXPORT DEMO")
    print("="*60)
    
    try:
        demo_simple_whiteboard()
        demo_shapes_whiteboard()
        demo_complex_whiteboard()
        
        print("\n" + "="*60)
        print("✅ ALL DEMOS COMPLETED!")
        print("="*60)
        print("\nGenerated videos:")
        print("  - demo_whiteboard_simple.mp4")
        print("  - demo_whiteboard_shapes.mp4")
        print("  - demo_whiteboard_complex.mp4")
        print("\nNote: These videos show progressive drawing animation")
        print("      with a drawing hand (if hand image is available)")
        print("\n")
        
    except Exception as e:
        print(f"\n❌ DEMO FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
