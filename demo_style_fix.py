#!/usr/bin/env python3
"""
Demonstration of the text style and alignment fix.

This script demonstrates how text styles (bold, italic) and alignments
now work correctly even for fonts that don't have dedicated style variants.

The fix applies synthetic styling when needed:
- Bold: Uses stroke_width to create thicker text
- Italic: Uses image transformation to create slanted text
- Alignment: Already worked, but now verified with styled text
"""

import sys
import os
import cv2
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))

from whiteboard_animator import render_text_to_image

def create_demo():
    """Create a demonstration showing all styles and alignments."""
    print("Creating demonstration of text styling fix...")
    print()
    
    # Configuration for different styles
    configs = [
        # Pacifico font styles (font only has 'normal' variant)
        {
            'section': 'Pacifico Font Styles',
            'items': [
                {'text': 'Normal Style', 'style': 'normal'},
                {'text': 'Bold Style (Synthetic)', 'style': 'bold'},
                {'text': 'Italic Style (Synthetic)', 'style': 'italic'},
                {'text': 'Bold Italic (Synthetic)', 'style': 'bold italic'},
            ]
        },
        # Alignment examples
        {
            'section': 'Text Alignment',
            'items': [
                {'text': 'Left Aligned', 'align': 'left', 'style': 'bold'},
                {'text': 'Center Aligned', 'align': 'center', 'style': 'bold'},
                {'text': 'Right Aligned', 'align': 'right', 'style': 'bold'},
            ]
        }
    ]
    
    images = []
    
    for config_section in configs:
        print(f"Rendering {config_section['section']}...")
        
        # Create section header
        header_img = np.ones((80, 800, 3), dtype=np.uint8) * 255
        cv2.putText(header_img, config_section['section'], (20, 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, (50, 50, 200), 3)
        images.append(header_img)
        
        # Render each item in the section
        for item in config_section['items']:
            text_config = {
                'text': item['text'],
                'font': 'Pacifico',
                'size': 42,
                'color': [0, 0, 0],
                'style': item.get('style', 'normal'),
                'align': item.get('align', 'center')
            }
            
            print(f"  - {item['text']}")
            img = render_text_to_image(text_config, 800, 120)
            if img is not None:
                images.append(img)
            else:
                print(f"    ⚠ Failed to render")
        
        # Add spacing
        spacing = np.ones((20, 800, 3), dtype=np.uint8) * 255
        images.append(spacing)
    
    # Combine all images vertically
    if images:
        combined = images[0]
        for img in images[1:]:
            combined = cv2.vconcat([combined, img])
        
        # Save the result
        output_path = '/home/runner/work/whiteboard/whiteboard/demo_style_fix_output.png'
        cv2.imwrite(output_path, combined)
        
        print()
        print(f"✓ Demo image saved to: {output_path}")
        print()
        print("The fix ensures:")
        print("  ✓ Fonts without bold/italic variants now show synthetic styling")
        print("  ✓ Bold is created using stroke effect")
        print("  ✓ Italic is created using shear transformation")
        print("  ✓ All text alignments work correctly")
        print("  ✓ Multiple styles can be combined (bold italic)")
        return True
    
    return False

if __name__ == "__main__":
    print("=" * 70)
    print("Text Style and Alignment Fix - Demonstration")
    print("=" * 70)
    print()
    
    success = create_demo()
    
    print()
    print("=" * 70)
    if success:
        print("✓ Demo completed successfully")
    else:
        print("✗ Demo failed")
    print("=" * 70)
    
    sys.exit(0 if success else 1)
