#!/usr/bin/env python3
"""
Demonstration of sceneCameras functionality.

This script demonstrates how to use sceneCameras to control the camera view
in a whiteboard animation scene. It shows:
1. Multiple text layers positioned at different locations
2. Camera movements to focus on different areas
3. Proper positioning of elements according to canvas coordinates
"""

import json
import os
import sys

def create_demo_scene():
    """Create a demo scene with multiple layers and sceneCameras."""
    
    scene = {
        "title": "Demo: sceneCameras",
        "description": "Demonstrates camera movements to show different parts of the canvas",
        "duration": 10,
        "canvas_width": 1920,
        "canvas_height": 1080,
        "layers": [
            # Top-left text
            {
                "id": "text-top-left",
                "type": "text",
                "mode": "draw",
                "position": {"x": 200, "y": 150},
                "z_index": 1,
                "skip_rate": 15,
                "text_config": {
                    "text": "Top Left Area",
                    "font": "Arial",
                    "size": 48,
                    "color": [255, 0, 0],
                    "align": "left",
                    "style": "bold"
                }
            },
            # Top-right text
            {
                "id": "text-top-right",
                "type": "text",
                "mode": "draw",
                "position": {"x": 1400, "y": 150},
                "z_index": 1,
                "skip_rate": 15,
                "text_config": {
                    "text": "Top Right Area",
                    "font": "Arial",
                    "size": 48,
                    "color": [0, 255, 0],
                    "align": "right",
                    "style": "bold"
                }
            },
            # Center text
            {
                "id": "text-center",
                "type": "text",
                "mode": "draw",
                "position": {"x": 960, "y": 540},
                "z_index": 2,
                "skip_rate": 12,
                "text_config": {
                    "text": "Center Area",
                    "font": "Arial",
                    "size": 64,
                    "color": [0, 0, 255],
                    "align": "center",
                    "style": "bold"
                }
            },
            # Bottom-left text
            {
                "id": "text-bottom-left",
                "type": "text",
                "mode": "draw",
                "position": {"x": 200, "y": 900},
                "z_index": 1,
                "skip_rate": 15,
                "text_config": {
                    "text": "Bottom Left Area",
                    "font": "Arial",
                    "size": 48,
                    "color": [255, 255, 0],
                    "align": "left",
                    "style": "bold"
                }
            },
            # Bottom-right text
            {
                "id": "text-bottom-right",
                "type": "text",
                "mode": "draw",
                "position": {"x": 1400, "y": 900},
                "z_index": 1,
                "skip_rate": 15,
                "text_config": {
                    "text": "Bottom Right Area",
                    "font": "Arial",
                    "size": 48,
                    "color": [255, 0, 255],
                    "align": "right",
                    "style": "bold"
                }
            }
        ],
        "sceneCameras": [
            # Camera 1: Start with wide view (zoom out to see everything)
            {
                "id": "camera-wide",
                "name": "Wide View",
                "position": {"x": 0.5, "y": 0.5},  # Center
                "zoom": 0.7,  # Zoom out to see more
                "duration": 2,
                "width": 1920,
                "height": 1080
            },
            # Camera 2: Focus on top-left
            {
                "id": "camera-top-left",
                "name": "Top Left Focus",
                "position": {"x": 0.2, "y": 0.2},
                "zoom": 1.2,
                "duration": 2,
                "transition_duration": 1,
                "easing": "ease_out"
            },
            # Camera 3: Focus on center
            {
                "id": "camera-center",
                "name": "Center Focus",
                "position": {"x": 0.5, "y": 0.5},
                "zoom": 1.5,
                "duration": 2,
                "transition_duration": 1,
                "easing": "ease_in_out"
            },
            # Camera 4: Focus on bottom-right
            {
                "id": "camera-bottom-right",
                "name": "Bottom Right Focus",
                "position": {"x": 0.8, "y": 0.8},
                "zoom": 1.2,
                "duration": 2,
                "transition_duration": 1,
                "easing": "ease_in"
            },
            # Camera 5: End with wide view again
            {
                "id": "camera-wide-end",
                "name": "Wide View End",
                "position": {"x": 0.5, "y": 0.5},
                "zoom": 0.7,
                "duration": 2,
                "transition_duration": 1,
                "easing": "ease_out"
            }
        ]
    }
    
    return scene


def main():
    """Generate the demo scene configuration and show usage instructions."""
    
    scene = create_demo_scene()
    
    # Save to file
    output_file = "demo_scene_cameras_config.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(scene, f, indent=2, ensure_ascii=False)
    
    print("="*70)
    print("🎬 Scene Cameras Demo Configuration Generated")
    print("="*70)
    print(f"\n✅ Configuration saved to: {output_file}")
    print("\nThis demo shows:")
    print("  • Multiple text layers positioned at different canvas locations")
    print("  • Camera movements using sceneCameras to focus on different areas")
    print("  • Wide view → Top Left → Center → Bottom Right → Wide view")
    print("  • Smooth transitions between camera positions")
    
    print("\n📋 Scene Details:")
    print(f"  - Canvas: {scene['canvas_width']}x{scene['canvas_height']}")
    print(f"  - Layers: {len(scene['layers'])}")
    print(f"  - Cameras: {len(scene['sceneCameras'])}")
    print(f"  - Total Duration: ~{sum(cam['duration'] for cam in scene['sceneCameras'])}s")
    
    print("\n🎥 To generate the video, run:")
    print(f"  python3 whiteboard_animator.py --config {output_file} \\")
    print("    --frame-rate 30 --skip-rate 20")
    
    print("\n💡 Key Features Demonstrated:")
    print("  1. sceneCameras field is automatically mapped to cameras")
    print("  2. Camera position uses relative coordinates (0.0-1.0)")
    print("  3. Layer positions use absolute pixel coordinates")
    print("  4. Zoom levels control how close/far the camera is")
    print("  5. Smooth transitions between camera views")
    
    print("\n" + "="*70)
    print("✨ Configuration ready! Run the command above to generate video.")
    print("="*70)


if __name__ == "__main__":
    main()
