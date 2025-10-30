#!/usr/bin/env python3
"""
Demo: Scene Composition with Camera Viewport
Demonstrates the compose_scene_with_camera function with practical examples.
"""

import cv2
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from whiteboard_animator import compose_scene_with_camera


def demo_presentation_scene():
    """Create a presentation-style scene with title, subtitle, and content."""
    print("\n" + "="*60)
    print("DEMO 1: Presentation Scene")
    print("="*60)
    
    scene_config = {
        'layers': [
            # Title
            {
                'id': 'title',
                'type': 'text',
                'text_config': {
                    'text': 'Scene Composition Demo',
                    'font': 'Arial',
                    'size': 80,
                    'color': (30, 50, 150),
                    'style': 'bold',
                    'align': 'center'
                },
                'position': {'x': 960, 'y': 150},
                'z_index': 2
            },
            # Subtitle
            {
                'id': 'subtitle',
                'type': 'text',
                'text_config': {
                    'text': 'Camera-Based Viewport Rendering',
                    'font': 'Arial',
                    'size': 40,
                    'color': (100, 100, 100),
                    'style': 'italic',
                    'align': 'center'
                },
                'position': {'x': 960, 'y': 250},
                'z_index': 2
            },
            # Background shape
            {
                'id': 'bg_box',
                'type': 'shape',
                'shape_config': {
                    'shape': 'rectangle',
                    'color': (200, 200, 200),
                    'fill_color': (245, 245, 250),
                    'stroke_width': 3,
                    'position': {'x': 960, 'y': 650},
                    'width': 1600,
                    'height': 600
                },
                'position': {'x': 960, 'y': 650},
                'z_index': 0
            },
            # Content points
            {
                'id': 'point1',
                'type': 'shape',
                'shape_config': {
                    'shape': 'circle',
                    'color': (50, 150, 50),
                    'fill_color': (150, 255, 150),
                    'stroke_width': 3,
                    'position': {'x': 300, 'y': 450},
                    'size': 30
                },
                'position': {'x': 300, 'y': 450},
                'z_index': 1
            },
            {
                'id': 'text1',
                'type': 'text',
                'text_config': {
                    'text': 'Multi-layer support',
                    'font': 'Arial',
                    'size': 36,
                    'color': (0, 0, 0)
                },
                'position': {'x': 400, 'y': 450},
                'z_index': 1
            },
            {
                'id': 'point2',
                'type': 'shape',
                'shape_config': {
                    'shape': 'circle',
                    'color': (50, 150, 50),
                    'fill_color': (150, 255, 150),
                    'stroke_width': 3,
                    'position': {'x': 300, 'y': 550},
                    'size': 30
                },
                'position': {'x': 300, 'y': 550},
                'z_index': 1
            },
            {
                'id': 'text2',
                'type': 'text',
                'text_config': {
                    'text': 'Camera viewport positioning',
                    'font': 'Arial',
                    'size': 36,
                    'color': (0, 0, 0)
                },
                'position': {'x': 400, 'y': 550},
                'z_index': 1
            },
            {
                'id': 'point3',
                'type': 'shape',
                'shape_config': {
                    'shape': 'circle',
                    'color': (50, 150, 50),
                    'fill_color': (150, 255, 150),
                    'stroke_width': 3,
                    'position': {'x': 300, 'y': 650},
                    'size': 30
                },
                'position': {'x': 300, 'y': 650},
                'z_index': 1
            },
            {
                'id': 'text3',
                'type': 'text',
                'text_config': {
                    'text': 'Easy transformations',
                    'font': 'Arial',
                    'size': 36,
                    'color': (0, 0, 0)
                },
                'position': {'x': 400, 'y': 650},
                'z_index': 1
            }
        ]
    }
    
    camera_config = {
        'width': 1920,
        'height': 1080,
        'position': {'x': 0.5, 'y': 0.5}
    }
    
    result = compose_scene_with_camera(
        scene_config,
        camera_config,
        scene_width=1920,
        scene_height=1080,
        background='#FFFFFF'
    )
    
    output_file = 'demo_presentation.png'
    cv2.imwrite(output_file, result)
    print(f"✅ Created: {output_file}")
    return output_file


def demo_diagram_scene():
    """Create a diagram with arrows and labels."""
    print("\n" + "="*60)
    print("DEMO 2: Diagram with Arrows")
    print("="*60)
    
    scene_config = {
        'layers': [
            # Central box
            {
                'id': 'center_box',
                'type': 'shape',
                'shape_config': {
                    'shape': 'rectangle',
                    'color': (50, 100, 200),
                    'fill_color': (150, 200, 255),
                    'stroke_width': 4,
                    'position': {'x': 960, 'y': 540},
                    'width': 200,
                    'height': 120
                },
                'position': {'x': 960, 'y': 540},
                'z_index': 1
            },
            {
                'id': 'center_label',
                'type': 'text',
                'text_config': {
                    'text': 'Core',
                    'font': 'Arial',
                    'size': 48,
                    'color': (0, 0, 0),
                    'style': 'bold',
                    'align': 'center'
                },
                'position': {'x': 960, 'y': 540},
                'z_index': 2
            },
            # Top box
            {
                'id': 'top_box',
                'type': 'shape',
                'shape_config': {
                    'shape': 'rectangle',
                    'color': (200, 100, 50),
                    'fill_color': (255, 200, 150),
                    'stroke_width': 4,
                    'position': {'x': 960, 'y': 200},
                    'width': 180,
                    'height': 100
                },
                'position': {'x': 960, 'y': 200},
                'z_index': 1
            },
            {
                'id': 'top_label',
                'type': 'text',
                'text_config': {
                    'text': 'Input',
                    'font': 'Arial',
                    'size': 40,
                    'color': (0, 0, 0),
                    'style': 'bold',
                    'align': 'center'
                },
                'position': {'x': 960, 'y': 200},
                'z_index': 2
            },
            # Bottom box
            {
                'id': 'bottom_box',
                'type': 'shape',
                'shape_config': {
                    'shape': 'rectangle',
                    'color': (50, 200, 100),
                    'fill_color': (150, 255, 200),
                    'stroke_width': 4,
                    'position': {'x': 960, 'y': 880},
                    'width': 180,
                    'height': 100
                },
                'position': {'x': 960, 'y': 880},
                'z_index': 1
            },
            {
                'id': 'bottom_label',
                'type': 'text',
                'text_config': {
                    'text': 'Output',
                    'font': 'Arial',
                    'size': 40,
                    'color': (0, 0, 0),
                    'style': 'bold',
                    'align': 'center'
                },
                'position': {'x': 960, 'y': 880},
                'z_index': 2
            },
            # Arrow from top to center
            {
                'id': 'arrow1',
                'type': 'arrow',
                'arrow_config': {
                    'start': [960, 260],
                    'end': [960, 470],
                    'color': (0, 0, 0),
                    'fill_color': (0, 0, 0),
                    'stroke_width': 3,
                    'arrow_size': 20
                },
                'position': {'x': 0, 'y': 0},
                'z_index': 0
            },
            # Arrow from center to bottom
            {
                'id': 'arrow2',
                'type': 'arrow',
                'arrow_config': {
                    'start': [960, 610],
                    'end': [960, 820],
                    'color': (0, 0, 0),
                    'fill_color': (0, 0, 0),
                    'stroke_width': 3,
                    'arrow_size': 20
                },
                'position': {'x': 0, 'y': 0},
                'z_index': 0
            }
        ]
    }
    
    camera_config = {
        'width': 1920,
        'height': 1080,
        'position': {'x': 0.5, 'y': 0.5}
    }
    
    result = compose_scene_with_camera(
        scene_config,
        camera_config,
        scene_width=1920,
        scene_height=1080,
        background='#F8F8F8'
    )
    
    output_file = 'demo_diagram.png'
    cv2.imwrite(output_file, result)
    print(f"✅ Created: {output_file}")
    return output_file


def demo_camera_pan():
    """Demonstrate camera panning across a large scene."""
    print("\n" + "="*60)
    print("DEMO 3: Camera Pan Across Scene")
    print("="*60)
    
    # Create a scene larger than the viewport
    scene_config = {
        'layers': [
            # Grid reference
            {
                'id': 'grid_label',
                'type': 'text',
                'text_config': {
                    'text': 'Scene Grid (3840x2160)',
                    'font': 'Arial',
                    'size': 60,
                    'color': (100, 100, 100),
                    'align': 'center'
                },
                'position': {'x': 1920, 'y': 100},
                'z_index': 1
            },
            # Markers at different positions
            {
                'id': 'marker_tl',
                'type': 'shape',
                'shape_config': {
                    'shape': 'circle',
                    'color': (255, 0, 0),
                    'fill_color': (255, 200, 200),
                    'stroke_width': 5,
                    'position': {'x': 400, 'y': 300},
                    'size': 80
                },
                'position': {'x': 400, 'y': 300},
                'z_index': 1
            },
            {
                'id': 'label_tl',
                'type': 'text',
                'text_config': {
                    'text': 'TOP\nLEFT',
                    'font': 'Arial',
                    'size': 40,
                    'color': (0, 0, 0),
                    'style': 'bold',
                    'align': 'center'
                },
                'position': {'x': 400, 'y': 300},
                'z_index': 2
            },
            {
                'id': 'marker_tr',
                'type': 'shape',
                'shape_config': {
                    'shape': 'circle',
                    'color': (0, 255, 0),
                    'fill_color': (200, 255, 200),
                    'stroke_width': 5,
                    'position': {'x': 3440, 'y': 300},
                    'size': 80
                },
                'position': {'x': 3440, 'y': 300},
                'z_index': 1
            },
            {
                'id': 'label_tr',
                'type': 'text',
                'text_config': {
                    'text': 'TOP\nRIGHT',
                    'font': 'Arial',
                    'size': 40,
                    'color': (0, 0, 0),
                    'style': 'bold',
                    'align': 'center'
                },
                'position': {'x': 3440, 'y': 300},
                'z_index': 2
            },
            {
                'id': 'marker_center',
                'type': 'shape',
                'shape_config': {
                    'shape': 'circle',
                    'color': (0, 0, 255),
                    'fill_color': (200, 200, 255),
                    'stroke_width': 5,
                    'position': {'x': 1920, 'y': 1080},
                    'size': 100
                },
                'position': {'x': 1920, 'y': 1080},
                'z_index': 1
            },
            {
                'id': 'label_center',
                'type': 'text',
                'text_config': {
                    'text': 'CENTER',
                    'font': 'Arial',
                    'size': 50,
                    'color': (0, 0, 0),
                    'style': 'bold',
                    'align': 'center'
                },
                'position': {'x': 1920, 'y': 1080},
                'z_index': 2
            }
        ]
    }
    
    # Create multiple camera views
    cameras = [
        ('left', {'x': 0.25, 'y': 0.5}),
        ('center', {'x': 0.5, 'y': 0.5}),
        ('right', {'x': 0.75, 'y': 0.5})
    ]
    
    output_files = []
    for name, position in cameras:
        camera_config = {
            'width': 1920,
            'height': 1080,
            'position': position
        }
        
        result = compose_scene_with_camera(
            scene_config,
            camera_config,
            scene_width=3840,
            scene_height=2160,
            background='#E8E8E8'
        )
        
        output_file = f'demo_camera_pan_{name}.png'
        cv2.imwrite(output_file, result)
        print(f"  ✓ Created: {output_file}")
        output_files.append(output_file)
    
    print(f"✅ Created {len(output_files)} camera views")
    return output_files


def demo_from_json():
    """Load scene from JSON configuration."""
    print("\n" + "="*60)
    print("DEMO 4: Load Scene from JSON")
    print("="*60)
    
    # Create a sample JSON configuration
    json_config = {
        "scene_width": 1920,
        "scene_height": 1080,
        "background": "#F0F8FF",
        "sceneCameras": [
            {
                "id": "main_camera",
                "width": 1920,
                "height": 1080,
                "position": {"x": 0.5, "y": 0.5},
                "isDefault": True
            }
        ],
        "layers": [
            {
                "id": "title",
                "type": "text",
                "text_config": {
                    "text": "Scene from JSON",
                    "font": "Arial",
                    "size": 72,
                    "color": [30, 80, 150],
                    "style": "bold",
                    "align": "center"
                },
                "position": {"x": 960, "y": 300},
                "z_index": 2
            },
            {
                "id": "shape1",
                "type": "shape",
                "shape_config": {
                    "shape": "rectangle",
                    "color": [100, 100, 200],
                    "fill_color": [200, 200, 255],
                    "stroke_width": 4,
                    "position": {"x": 600, "y": 600},
                    "width": 300,
                    "height": 200
                },
                "position": {"x": 600, "y": 600},
                "z_index": 1,
                "scale": 1.0,
                "opacity": 0.9
            },
            {
                "id": "shape2",
                "type": "shape",
                "shape_config": {
                    "shape": "circle",
                    "color": [200, 100, 100],
                    "fill_color": [255, 200, 200],
                    "stroke_width": 4,
                    "position": {"x": 1320, "y": 600},
                    "size": 100
                },
                "position": {"x": 1320, "y": 600},
                "z_index": 1,
                "opacity": 0.9
            }
        ]
    }
    
    # Save JSON
    json_file = 'demo_scene_config.json'
    with open(json_file, 'w') as f:
        json.dump(json_config, f, indent=2)
    print(f"  📄 Created JSON config: {json_file}")
    
    # Load and render
    with open(json_file, 'r') as f:
        config = json.load(f)
    
    result = compose_scene_with_camera(
        config,
        camera_config=None,  # Will use sceneCameras
        scene_width=config['scene_width'],
        scene_height=config['scene_height'],
        background=config['background']
    )
    
    output_file = 'demo_from_json.png'
    cv2.imwrite(output_file, result)
    print(f"✅ Created: {output_file}")
    return output_file


if __name__ == '__main__':
    print("\n" + "="*70)
    print("  SCENE COMPOSITION WITH CAMERA - DEMONSTRATION")
    print("="*70)
    
    try:
        # Run all demos
        demo_presentation_scene()
        demo_diagram_scene()
        demo_camera_pan()
        demo_from_json()
        
        print("\n" + "="*70)
        print("✅ ALL DEMOS COMPLETED SUCCESSFULLY!")
        print("="*70)
        print("\nGenerated files:")
        print("  - demo_presentation.png")
        print("  - demo_diagram.png")
        print("  - demo_camera_pan_left.png")
        print("  - demo_camera_pan_center.png")
        print("  - demo_camera_pan_right.png")
        print("  - demo_from_json.png")
        print("  - demo_scene_config.json")
        print("\nSee SCENE_COMPOSITION_GUIDE.md for detailed documentation.")
        print("")
        
    except Exception as e:
        print(f"\n❌ DEMO FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
