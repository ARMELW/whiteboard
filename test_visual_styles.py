#!/usr/bin/env python3
"""Visual test to compare different text styles and alignments."""

import sys
import os
import cv2

sys.path.insert(0, os.path.dirname(__file__))

from whiteboard_animator import render_text_to_image

def test_visual_comparison():
    """Create a visual comparison of different styles."""
    print("Creating visual comparison of text styles...")
    
    # Test configurations
    configs = [
        {
            'name': 'Pacifico-Normal',
            'text_config': {
                'text': 'Normal Style',
                'font': 'Pacifico',
                'size': 48,
                'color': [0, 0, 0],
                'style': 'normal',
                'align': 'center'
            }
        },
        {
            'name': 'Pacifico-Bold',
            'text_config': {
                'text': 'Bold Style',
                'font': 'Pacifico',
                'size': 48,
                'color': [0, 0, 0],
                'style': 'bold',
                'align': 'center'
            }
        },
        {
            'name': 'Pacifico-Italic',
            'text_config': {
                'text': 'Italic Style',
                'font': 'Pacifico',
                'size': 48,
                'color': [0, 0, 0],
                'style': 'italic',
                'align': 'center'
            }
        },
        {
            'name': 'Pacifico-BoldItalic',
            'text_config': {
                'text': 'Bold Italic',
                'font': 'Pacifico',
                'size': 48,
                'color': [0, 0, 0],
                'style': 'bold italic',
                'align': 'center'
            }
        },
        {
            'name': 'DejaVu-Left',
            'text_config': {
                'text': 'Left Aligned',
                'font': 'DejaVuSans',
                'size': 48,
                'color': [0, 0, 0],
                'style': 'bold',
                'align': 'left'
            }
        },
        {
            'name': 'DejaVu-Center',
            'text_config': {
                'text': 'Center Aligned',
                'font': 'DejaVuSans',
                'size': 48,
                'color': [0, 0, 0],
                'style': 'bold',
                'align': 'center'
            }
        },
        {
            'name': 'DejaVu-Right',
            'text_config': {
                'text': 'Right Aligned',
                'font': 'DejaVuSans',
                'size': 48,
                'color': [0, 0, 0],
                'style': 'bold',
                'align': 'right'
            }
        }
    ]
    
    # Render each configuration
    images = []
    for config in configs:
        print(f"  Rendering {config['name']}...")
        img = render_text_to_image(config['text_config'], 800, 150)
        if img is not None:
            images.append((config['name'], img))
        else:
            print(f"    ✗ Failed to render {config['name']}")
            return False
    
    # Combine images vertically
    if images:
        combined = images[0][1]
        for name, img in images[1:]:
            combined = cv2.vconcat([combined, img])
        
        # Add labels
        for i, (name, _) in enumerate(images):
            y_pos = i * 150 + 70
            cv2.putText(combined, name, (10, y_pos + 100), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (128, 128, 128), 2)
        
        # Save the result
        output_path = '/home/runner/work/whiteboard/whiteboard/test_visual_styles_output.png'
        cv2.imwrite(output_path, combined)
        print(f"\n✓ Visual comparison saved to: {output_path}")
        return True
    
    return False

if __name__ == "__main__":
    print("=" * 70)
    print("Visual Text Style and Alignment Test")
    print("=" * 70)
    print()
    
    success = test_visual_comparison()
    
    print()
    print("=" * 70)
    if success:
        print("✓ Visual test completed successfully")
    else:
        print("✗ Visual test failed")
    print("=" * 70)
    
    sys.exit(0 if success else 1)
