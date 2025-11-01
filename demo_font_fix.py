#!/usr/bin/env python3
"""
Demonstration of the font size fix for video rendering with camera zoom.
This recreates a scenario similar to the user's reported issue.
"""

import cv2
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from whiteboard_animator import compose_scene_with_camera

def create_demo_scene():
    """Create a demo scene with text similar to the user's example."""
    return {
        'layers': [
            {
                'id': 'demo_text',
                'type': 'text',
                'text_config': {
                    'text': 'Votre texte ici',
                    'font': 'Arial',
                    'size': 80,  # Large font size like in the screenshots
                    'color': (0, 0, 0),
                    'style': 'normal',
                    'align': 'center'
                },
                'position': {'x': 960, 'y': 540},  # Center of 1920x1080
                'anchor_point': 'center',
                'z_index': 1,
                'visible': True
            }
        ]
    }

def main():
    print("=" * 70)
    print("FONT SIZE FIX DEMONSTRATION")
    print("=" * 70)
    print()
    print("This demo shows how text is now rendered correctly with camera zoom.")
    print("The fix ensures font sizes are respected and text remains crisp.")
    print()
    
    scene = create_demo_scene()
    
    # Test case 1: Normal view (no zoom)
    print("📹 Rendering with no zoom (1.0x)...")
    camera_normal = {
        'width': 800,
        'height': 450,
        'position': {'x': 0.5, 'y': 0.5},
        'zoom': 1.0
    }
    result_normal = compose_scene_with_camera(
        scene, camera_normal, scene_width=1920, scene_height=1080, verbose=False
    )
    cv2.imwrite('demo_font_normal.png', result_normal)
    print("   ✅ Saved: demo_font_normal.png")
    
    # Test case 2: Zoomed in view (like in video rendering)
    print("\n📹 Rendering with 1.5x zoom (typical for video)...")
    camera_zoomed = {
        'width': 800,
        'height': 450,
        'position': {'x': 0.5, 'y': 0.5},
        'zoom': 1.5
    }
    result_zoomed = compose_scene_with_camera(
        scene, camera_zoomed, scene_width=1920, scene_height=1080, verbose=False
    )
    cv2.imwrite('demo_font_zoomed.png', result_zoomed)
    print("   ✅ Saved: demo_font_zoomed.png")
    
    # Test case 3: High zoom (2x)
    print("\n📹 Rendering with 2.0x zoom (close-up)...")
    camera_close = {
        'width': 800,
        'height': 450,
        'position': {'x': 0.5, 'y': 0.5},
        'zoom': 2.0
    }
    result_close = compose_scene_with_camera(
        scene, camera_close, scene_width=1920, scene_height=1080, verbose=False
    )
    cv2.imwrite('demo_font_close.png', result_close)
    print("   ✅ Saved: demo_font_close.png")
    
    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)
    print("✅ All renderings completed successfully!")
    print()
    print("Compare the images:")
    print("  - demo_font_normal.png  : Text at normal size")
    print("  - demo_font_zoomed.png  : Text 1.5x larger, crisp and clear")
    print("  - demo_font_close.png   : Text 2x larger, crisp and clear")
    print()
    print("The fix ensures text is rendered at the correct font size")
    print("for the zoom level, avoiding blurry scaling artifacts.")
    print("=" * 70)

if __name__ == '__main__':
    main()
