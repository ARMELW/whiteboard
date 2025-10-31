#!/usr/bin/env python3
"""
Demo: Camera Zoom and Position
Demonstrates the camera zoom and position fix with visual examples.
"""

import cv2
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from whiteboard_animator import compose_scene_with_camera


def create_demo_scene():
    """Create a simple demo scene with multiple elements."""
    return {
        'layers': [
            # Center circle
            {
                'id': 'center',
                'type': 'shape',
                'shape_config': {
                    'shape': 'circle',
                    'color': (0, 0, 255),
                    'fill_color': (100, 100, 255),
                    'stroke_width': 3,
                    'position': {'x': 960, 'y': 540},
                    'size': 50
                },
                'position': {'x': 0, 'y': 0},
                'z_index': 2
            },
            # Top-left marker
            {
                'id': 'tl',
                'type': 'shape',
                'shape_config': {
                    'shape': 'rectangle',
                    'color': (0, 255, 0),
                    'fill_color': (100, 255, 100),
                    'stroke_width': 2,
                    'position': {'x': 200, 'y': 200},
                    'width': 50,
                    'height': 50
                },
                'position': {'x': 0, 'y': 0},
                'z_index': 1
            },
            # Bottom-right marker
            {
                'id': 'br',
                'type': 'shape',
                'shape_config': {
                    'shape': 'rectangle',
                    'color': (255, 0, 0),
                    'fill_color': (255, 100, 100),
                    'stroke_width': 2,
                    'position': {'x': 1720, 'y': 880},
                    'width': 50,
                    'height': 50
                },
                'position': {'x': 0, 'y': 0},
                'z_index': 1
            },
            # Grid lines
            {
                'id': 'grid_h',
                'type': 'shape',
                'shape_config': {
                    'shape': 'line',
                    'color': (200, 200, 200),
                    'stroke_width': 1,
                    'start': [0, 540],
                    'end': [1920, 540]
                },
                'position': {'x': 0, 'y': 0},
                'z_index': 0
            },
            {
                'id': 'grid_v',
                'type': 'shape',
                'shape_config': {
                    'shape': 'line',
                    'color': (200, 200, 200),
                    'stroke_width': 1,
                    'start': [960, 0],
                    'end': [960, 1080]
                },
                'position': {'x': 0, 'y': 0},
                'z_index': 0
            }
        ]
    }


def demo_zoom_levels():
    """Demonstrate different zoom levels."""
    print("\n" + "="*60)
    print("DEMO: Camera Zoom Levels")
    print("="*60)
    
    scene = create_demo_scene()
    
    zoom_levels = [
        {'zoom': 0.5, 'desc': 'Zoom 0.5x (zoomed out - see more)'},
        {'zoom': 1.0, 'desc': 'Zoom 1.0x (normal view)'},
        {'zoom': 1.5, 'desc': 'Zoom 1.5x (zoomed in)'},
        {'zoom': 2.0, 'desc': 'Zoom 2.0x (zoomed in more)'},
    ]
    
    for level in zoom_levels:
        print(f"\n📷 {level['desc']}")
        
        camera = {
            'width': 800,
            'height': 450,
            'position': {'x': 0.5, 'y': 0.5},  # Center
            'zoom': level['zoom']
        }
        
        result = compose_scene_with_camera(
            scene,
            camera,
            scene_width=1920,
            scene_height=1080,
            background='#FFFFFF',
            verbose=False
        )
        
        output_file = f"demo_zoom_{level['zoom']:.1f}x.png"
        cv2.imwrite(output_file, result)
        print(f"   ✓ Saved: {output_file}")


def demo_camera_positions():
    """Demonstrate different camera positions with zoom."""
    print("\n" + "="*60)
    print("DEMO: Camera Positions with Zoom")
    print("="*60)
    
    scene = create_demo_scene()
    
    positions = [
        {'x': 0.25, 'y': 0.25, 'desc': 'Top-left'},
        {'x': 0.75, 'y': 0.25, 'desc': 'Top-right'},
        {'x': 0.5, 'y': 0.5, 'desc': 'Center'},
        {'x': 0.25, 'y': 0.75, 'desc': 'Bottom-left'},
        {'x': 0.75, 'y': 0.75, 'desc': 'Bottom-right'},
    ]
    
    for pos in positions:
        print(f"\n📍 Position: {pos['desc']} ({pos['x']}, {pos['y']}) with zoom 1.5x")
        
        camera = {
            'width': 800,
            'height': 450,
            'position': {'x': pos['x'], 'y': pos['y']},
            'zoom': 1.5
        }
        
        result = compose_scene_with_camera(
            scene,
            camera,
            scene_width=1920,
            scene_height=1080,
            background='#FFFFFF',
            verbose=False
        )
        
        output_file = f"demo_pos_{pos['desc'].lower().replace('-', '_')}.png"
        cv2.imwrite(output_file, result)
        print(f"   ✓ Saved: {output_file}")


def demo_zoom_animation_frames():
    """Create frames for a smooth zoom animation."""
    print("\n" + "="*60)
    print("DEMO: Zoom Animation Frames")
    print("="*60)
    
    scene = create_demo_scene()
    
    print("\n🎬 Creating smooth zoom animation frames...")
    
    # Create frames from zoom 0.5 to 2.0
    zoom_steps = 20
    for i in range(zoom_steps + 1):
        progress = i / zoom_steps
        zoom = 0.5 + (2.0 - 0.5) * progress
        
        camera = {
            'width': 800,
            'height': 450,
            'position': {'x': 0.5, 'y': 0.5},
            'zoom': zoom
        }
        
        result = compose_scene_with_camera(
            scene,
            camera,
            scene_width=1920,
            scene_height=1080,
            background='#FFFFFF',
            verbose=False
        )
        
        output_file = f"demo_zoom_anim_frame_{i:03d}.png"
        cv2.imwrite(output_file, result)
        
        if i % 5 == 0:
            print(f"   ✓ Frame {i:3d}/20: zoom={zoom:.2f}x")
    
    print(f"\n   💡 Created {zoom_steps + 1} frames for zoom animation")
    print(f"   You can use ffmpeg to create a video:")
    print(f"   ffmpeg -framerate 10 -i demo_zoom_anim_frame_%03d.png -c:v libx264 zoom_animation.mp4")


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🎥 CAMERA ZOOM AND POSITION DEMO")
    print("="*60)
    print("\nThis demo shows how camera zoom and position work together")
    print("to create precise viewport control in scene rendering.")
    
    try:
        demo_zoom_levels()
        demo_camera_positions()
        demo_zoom_animation_frames()
        
        print("\n" + "="*60)
        print("✅ DEMO COMPLETED SUCCESSFULLY!")
        print("="*60)
        print("\nCheck the generated PNG files to see the results.")
        
    except Exception as e:
        print(f"\n❌ DEMO FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
